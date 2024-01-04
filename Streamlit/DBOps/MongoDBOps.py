from subprocess import call
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient, UpdateOne
import pandas as pd
import subprocess
import os
import json
import numpy as np
from datetime import datetime, timedelta


class MongoDBHandler:
    def __init__(self, client):
        self.client = client
        self.db = None
        self.collection = None
        self.pipeline = []
        self.stage_dict = {"$match": {}, "$project": {}}

    def load_database(self,
                      database_name
                      ):
        self.db = self.client[database_name]

    def load_collection(self,
                        collection_name
                        ):
        if self.db is not None:
            self.collection = self.db[collection_name]
        else:
            print("Please load database first")

    # CREATE
    def create_database(self, database_name):
        existing_databases = self.client.list_database_names()
        if database_name in existing_databases:
            print("The database already exists.")
        else:
            self.db = self.client[database_name]
            print("Creating a new database.")

    def create_collection(self, collection_name):
        if self.db is not None:
            self.collection = self.db[collection_name]
        else:
            print("Please load database first")

    def add_document_to_collection(self, document):
        """

        :param document: Document to be inserted in collection (Type: dict)
        :return:
        """
        result = self.collection.insert_one(document)
        if result.inserted_id:
            print("Document added successfully")
            return 1
        else:
            return 0

    def append_list_values_to_level_1_collection_list_field(self, document_filter, field_to_update, new_values):
        """
        Find a document by its filter and append a list of values to a list field.

        Parameters:
        - document_filter: dict, filter condition to find the document(s) to update
        - field_to_update: str, the name of the list field to append to
        - new_values: list, the list of values to append to the list
        """
        update_operation = {'$push': {field_to_update: {'$each': new_values}}}

        result = self.collection.update_one(document_filter, update_operation)

        if result.modified_count > 0:
            print(f"Appended {len(new_values)} items to the list in document matching {document_filter}")
        else:
            print(f"No document matching {document_filter} found")

    def generate_id(self, counter):
        try:
            self.collection.insert_one({"_id": counter, "sequence_value": 0})
        except DuplicateKeyError:
            pass

        result = self.collection.find_one_and_update(
            {"_id": counter},
            {"$inc": {"sequence_value": 1}},
            return_document=True
        )
        return result['sequence_value']

    # READ QUERIES

    def get_field_values_from_level_1_collection(self, field_names, collection_filter={}, project_id=False, unique=True):
        """
        :param field_names: Specify the list of field for which you wish to list all associated values.
        :param collection_filter: filter for narrowing down documents in a collection.
        :return: Enumerate all values associated with a specific field within the documents across
        the entire collection.
        """

        print("getting field value list from collection")
        pipeline = [
            {"$match": collection_filter},
            {"$project": {field_name: f'${field_name}' for field_name in field_names}}
        ]
        if project_id is False:
            pipeline[1]["$project"]["_id"] = 0

        result = list(self.collection.aggregate(pipeline))
        if len(field_names) == 1:
            field_values = [doc[field_names[0]] for doc in result]
            if unique is True:
                field_values = list(set(field_values))

            return field_values
        else:
            return result

    def get_field_values_from_level_2_collection(self, collection_field_name, array_field_name, collection_filter={}):
        """
        :param collection_field_name: This is the field name within a document in a collection that holds an array of
        documents as its value.
        :param array_field_name: This is the field name within a document that is inside the array of document.
        :param collection_filter: This is the filter used to narrow down documents for which values are required from a
        nested array.
        :return: enumerates values of a specific field in all the documents from an array of documents stored within a
        field of a filtered documents in a collection.
        """
        pipeline = [
            {"$match": collection_filter},
            {"$unwind": f"${collection_field_name}"},
            {"$project": {f"{collection_field_name}.{array_field_name}": 1, "_id": 0}}
        ]
        result = self.collection.aggregate(pipeline)
        return [doc[collection_field_name][array_field_name] for doc in list(self.collection.aggregate(pipeline))]

    def get_document_from_level_1_collection(self, document_filter={}):
        document = self.collection.find_one(document_filter)
        return document

    def get_document_from_level_2_collection(self,
                                             nested_array,
                                             collection_filter={},
                                             array_document_filter={"field_name": None, "field_value": None}
                                             ):
        """

        :param nested_array: This is the field name within a document in a collection that stores an array of documents.
        :param collection_filter: This is the filter used to narrow down documents for which values are required from a
        nested array.
        :param array_document_filter: These filters are based on the fields within the documents contained in an array,
        aiming to retrieve specific documents from the array.
        :return: A singular document extracted from an array of documents stored within a field of a filtered documents
        in a collection.
        """
        pipeline = [
            {"$match": collection_filter},  # Match the document by its ID
            {"$project": {
                nested_array: {
                    "$filter": {
                        "input": f"${nested_array}",
                        "as": nested_array,
                        "cond": {"$eq": [f"$${nested_array}.{array_document_filter['field_name']}",
                                         array_document_filter['field_value']]}
                    }
                },
                "_id": 0
            }}]
        result = self.collection.aggregate(pipeline)
        return list(result)[0][nested_array][0]

    def get_field_values_from_level_1_document(self, l_1_c_filter, l_1_d_field_name):
        pipeline = [
            {"$match": l_1_c_filter},
            {"$project": {f"{l_1_d_field_name}": f"${l_1_d_field_name}", "_id": 0}}
        ]
        result = list(self.collection.aggregate(pipeline))[0][l_1_d_field_name]
        return result

    def get_collection_dataframe(self, collection_filter={}, exclude_columns=[], **kwargs):
        print(collection_filter)
        if "time_filter" in kwargs:
            self.apply_time_filter(timestamp_field="date",
                                   start_datetime=kwargs["time_filter"]["start_date"],
                                   end_datetime=kwargs["time_filter"]["end_date"]
                                   )

        if collection_filter:
            self.apply_multiselect_filter(multiselect_filter_dict=collection_filter)
        if exclude_columns:
            self.project_specific_columns(exclude_columns=exclude_columns)
        else:
            self.project_except_id()
        self.create_pipeline()
        cursor = self.collection.aggregate(self.pipeline)
        data = list(cursor)
        df = pd.DataFrame(data)
        return df

    def apply_time_filter(self, timestamp_field, start_datetime, end_datetime):
        self.stage_dict["$match"][timestamp_field] = {
                "$gte": start_datetime,
                "$lt": end_datetime
            }

    def apply_multiselect_filter(self, multiselect_filter_dict):
        for column, values in multiselect_filter_dict.items():
            self.stage_dict["$match"][column] = {"$in": values}

    def project_specific_columns(self, exclude_columns):
        for field in exclude_columns:
            self.stage_dict["$project"][field] = 0

    def project_except_id(self):
        self.stage_dict["$project"] = {"_id": 0}

    def create_pipeline(self):
        if self.stage_dict["$match"]:
            self.pipeline.append({"$match": self.stage_dict["$match"]})
        if self.stage_dict["$project"]:
            self.pipeline.append({"$project": self.stage_dict["$project"]})


    # UPDATE



    # MODIFY


    def add_field_to_collection(self, filter_condition, field_name, field_value):
        """
        Add a field and its corresponding value to all documents in a collection.

        Parameters:
        - filter_condition:
        - field_name: str, the name of the new field
        - field_value: any, the value to set for the new field
        """
        update_operation = {'$set': {field_name: field_value}}

        result = self.collection.update_many(filter_condition, update_operation)

        print(f"Added field '{field_name}' with value '{field_value}' to {result.modified_count} document(s)")

    # MISC
    def rename_database(self, old_db_name, new_db_name):
        # Step 1: Create a dump of the old database
        call(['mongodump', '--db', old_db_name])

        # Step 2: Restore the dump to a new database
        self.client.drop_database(new_db_name)
        call(['mongorestore', '--db', new_db_name, 'dump/' + old_db_name])

        # Step 3: (Optional) Drop the old database
        self.client.drop_database(old_db_name)

    def create_duplicate_field(self, field_mappings):
        """
        Rename fields in all documents of a collection.

        Parameters:
        - db: pymongo.database.Database, the MongoDB database
        - collection_name: str, the name of the collection
        - field_mappings: dict, a dictionary mapping old field names to new field names
        """

        for document in self.collection.find():
            updated_document = {}
            for old_field, new_field in field_mappings.items():
                if old_field in document:
                    updated_document[new_field] = document[old_field]
                else:
                    updated_document[new_field] = None  # Handle missing fields

            # Update the document with renamed fields
            self.collection.update_one({'_id': document['_id']}, {'$set': updated_document})


    def transfer_collection(self, source_db, source_collection, destination_db, destination_collection):
        source_db = self.client[source_db]
        destination_db = self.client[destination_db]
        source_collection = source_db[source_collection]
        destination_collection = destination_db[destination_collection]
        documents_to_transfer = source_collection.find({})
        destination_collection.insert_many(documents_to_transfer)

    # IMPORT EXPORT
    def export_database_subprocess(self, database_names, output_directory):
        def dump():
            db = self.client[database_name]
            dump_command = f"mongodump --db {database_name} --out {output_directory}"
            subprocess.run(dump_command, shell=True)

        if len(database_names) == 0:
            database_names = client.list_database_names()

        for database_name in database_names:
            dump()
            print(f"Database '{database_name}' exported successfully to '{output_directory}'")

    def export_database(self, database_name, output_directory):
        # Access the database
        db = self.client[database_name]

        # Create a directory for the database dump
        db_dump_directory = os.path.join(output_directory, database_name)
        os.makedirs(db_dump_directory, exist_ok=True)

        # Loop through each collection and export it
        for collection_name in db.list_collection_names():
            self.export_collection(database_name, collection_name, db_dump_directory)

        print(f"Database '{database_name}' exported successfully to '{db_dump_directory}'")

    def export_collection(self, database_name, collection_name, output_directory):
        # Access the collection
        collection = self.client[database_name][collection_name]

        # Export the collection data to a JSON file
        export_file_path = os.path.join(output_directory, f"{collection_name}.json")
        with open(export_file_path, 'w') as export_file:
            for document in collection.find():
                export_file.write(json.dumps(document, default=str) + '\n')

        print(f"Collection '{collection_name}' exported successfully to '{export_file_path}'")

    def export_all_databases(self, output_directory):
        # Get the list of all databases
        database_names = self.client.list_database_names()

        # Loop through each database and export it
        for database_name in database_names:
            self.export_database(database_name, output_directory)

        print(f"All databases exported successfully to '{output_directory}'")

    def import_database(self, database_name, input_directory):
        # Access the database
        db = self.client[database_name]

        # Loop through each collection file and import it
        for collection_file in os.listdir(input_directory):
            if collection_file.endswith(".json"):
                collection_name = os.path.splitext(collection_file)[0]
                self.import_collection(database_name, collection_name, input_directory)

        print(f"Database '{database_name}' imported successfully from '{input_directory}'")

    def import_collection(self, database_name, collection_name, input_directory):
        # Access the collection
        collection = self.client[database_name][collection_name]

        # Import the collection data from a JSON file
        import_file_path = os.path.join(input_directory, f"{collection_name}.json")
        with open(import_file_path, 'r') as import_file:
            for line in import_file:
                document = json.loads(line)
                collection.insert_one(document)

        print(f"Collection '{collection_name}' imported successfully from '{import_file_path}'")

    def import_all_databases(self, input_directory):
        # Loop through each database directory and import it
        for database_directory in os.listdir(input_directory):
            database_path = os.path.join(input_directory, database_directory)
            if os.path.isdir(database_path):
                database_name = database_directory
                self.import_database(database_name, database_path)

        print(f"All databases imported successfully from '{input_directory}'")

    def import_documents_from_csv(self, csv_path, collection_name, database_name):
        self.load_database(database_name)
        self.load_collection(collection_name)
        df = pd.read_csv(csv_path)
        data = df.to_dict(orient='records')
        self.collection.insert_many(data)

    from pymongo import MongoClient

    def sync_collections(self, destination_client):
        # Connect to MongoDB clients
        source = self.client
        destination = MongoClient(destination_client)

        # Get database names from both clients
        source_dbs = source.list_database_names()
        destination_dbs = destination.list_database_names()

        # Compare databases and sync collections
        for db_name in source_dbs:
            if db_name in destination_dbs:
                source_db = source[db_name]
                destination_db = destination[db_name]

                source_collections = source_db.list_collection_names()
                destination_collections = destination_db.list_collection_names()

                for collection_name in source_collections:
                    if collection_name in destination_collections:
                        # Collection exists in both databases
                        source_collection = source_db[collection_name]
                        destination_collection = destination_db[collection_name]

                        # Compare documents and sync
                        for doc in source_collection.find():
                            existing_doc = destination_collection.find_one({"_id": doc["_id"]})
                            if existing_doc:
                                if existing_doc != doc:
                                    # If documents are different, update the document
                                    destination_collection.replace_one({"_id": doc["_id"]}, doc)
                            else:
                                # If document doesn't exist, insert it
                                destination_collection.insert_one(doc)
                    else:
                        # Collection exists in source but not in destination
                        print(f"Copying collection {collection_name} from source to destination...")
                        source_collection = source_db[collection_name]
                        destination_db.create_collection(collection_name)
                        destination_collection = destination_db[collection_name]

                        documents = source_collection.find()
                        destination_collection.insert_many(documents)
            else:
                # Database exists in source but not in destination
                print(f"Copying database {db_name} from source to destination...")
                source_db = source[db_name]
                destination_db = destination[db_name]

                collections = source_db.list_collection_names()
                for collection_name in collections:
                    source_collection = source_db[collection_name]
                    destination_db.create_collection(collection_name)
                    destination_collection = destination_db[collection_name]

                    documents = source_collection.find()
                    try:
                        destination_collection.insert_many(documents)
                    except:
                        pass

        # Close connections
        source.close()
        destination.close()


class MongoDBErrorHandler:
    def __init__(self, client):
        self.client = client
        self.db = self.client["common"]
        self.collection = self.db["ERROR_LOG"]

    def log_error(self, error_message):
        error_document = {
            "timestamp": datetime.utcnow(),
            "error_message": error_message
        }

        # Insert the document into the collection
        self.collection.insert_one(error_document)




if __name__ == "__main__":
    client = MongoClient("mongodb://10.11.10.72:27017/")
    # client = MongoClient("mongodb://10.11.10.95:27017/")

    datahandler = MongoDBHandler(client)

    # datahandler.load_database("testing_history")
    # datahandler.load_collection("timeline")
    # a = sorted(datahandler.get_field_values_from_level_1_collection(field_names=["Dept"]))

    # csv_path = "../data/emission_csv/single_line_csv_etr_entry.csv"
    # datahandler.import_documents_from_csv(csv_path, "emission_dashboard", "testing_history")

    # datahandler.load_database("testing_history")
    # datahandler.load_collection("timeline")
    # start_time = (datetime.now() - timedelta(days=30)).strftime('%d-%m-%Y %H:%M:%S')
    # end_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    # s = "20-11-2023 00:00:00"
    # e = "20-12-2023 00:00:00"
    # datahandler.apply_time_filter(timestamp_field="date", start_datetime=s, end_datetime=e)

    # df = datahandler.get_collection_dataframe(
    #     collection_filter={"model": ["M1"]},
    #     time_filter={"start_date": s,
    #                  "end_date": e}
    # )

    # df = datahandler.get_collection_dataframe(
    #     collection_filter={"model": ["M1"]})

    # datahandler.export_all_databases(output_directory=r"D:\BAL Projects\01_Misc\MN_Colab\Streamlit\db")
    # datahandler.import_all_databases(r"D:\BAL Projects\01_Misc\MN_Colab\Streamlit\db")

    # datahandler.transfer_collection("CAL", "DATASETS", "CAL", "dataset_log")

    source_uri = client
    destination_uri = "mongodb://localhost:27017"
    datahandler.sync_collections(destination_uri)


