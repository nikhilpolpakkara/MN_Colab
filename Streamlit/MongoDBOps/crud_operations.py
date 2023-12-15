from subprocess import call
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient, UpdateOne
import pandas as pd


class MongoDBHandler:
    def __init__(self, client):
        self.client = client
        self.db = None
        self.collection = None

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

    # CREATE QUERIES
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

        :param document: Document to be inserted in collection
        :return:
        """
        result = self.collection.insert_one(document)
        if result.inserted_id:
            print("Document added successfully")
            return 1
        else:
            return 0

    # READ QUERIES

    def get_field_values_from_level_1_collection(self, field_names, collection_filter={}, project_id=False):
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
                "test_activity": {
                    "$filter": {
                        "input": f"${nested_array}",
                        "as": "activity",
                        "cond": {"$eq": [f"$$activity.{array_document_filter['field_name']}",
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

    # UPDATE

    def get_next_id(self, counter):
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

    def append_to_list_by_id(self, document_id, field_to_update, new_value):
        """
        Find a document by its _id and append a value to a list field.

        Parameters:
        - collection: pymongo.collection.Collection, the MongoDB collection
        - document_id: any, the _id value of the document to update
        - field_to_update: str, the name of the list field to append to
        - new_value: any, the value to append to the list
        """
        filter_condition = {'_id': document_id}
        update_operation = {'$push': {field_to_update: new_value}}

        result = self.collection.update_one(filter_condition, update_operation)

        if result.modified_count > 0:
            print(f"Appended {new_value} to the list in document with _id {document_id}")
        else:
            print(f"No document with _id {document_id} found")

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

    def get_collection_dataframe(self):
        pipeline = [
            {"$project": {
                "section_width": 0,
                "aspect_ratio": 0,
                "rim_dia": 0
            }
            }]
        cursor = self.collection.aggregate(pipeline)
        data = list(cursor)
        df = pd.DataFrame(data)
        return df

    def transfer_collection(self, source_db, source_collection, destination_db, destination_collection):
        source_db = self.client[source_db]
        destination_db = self.client[destination_db]
        source_collection = source_db[source_collection]
        destination_collection = destination_db[destination_collection]
        documents_to_transfer = source_collection.find({})
        destination_collection.insert_many(documents_to_transfer)


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    datahandler = MongoDBHandler(client)

