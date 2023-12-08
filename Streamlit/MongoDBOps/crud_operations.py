from subprocess import call
from pymongo.errors import DuplicateKeyError

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
            return 1
        else:
            return 0

    # READ QUERIES

    def get_document_from_collection(self, document_filter={}):
        document = self.collection.find_one(document_filter)
        return document

    def get_field_values_from_collection(self, field_name):
        """

        :param field_name:
        :return: List of field values for the field name in the collection of all documents
        """
        pipeline = [{"$project": {"_id": 0, field_name: f'${field_name}'}}]
        result = list(self.collection.aggregate(pipeline))
        print(result)
        field_values = [doc[field_name] for doc in result]
        return field_values

    def get_document_from_nested_array(self,
                                       nested_array,
                                       collection_filter={},
                                       array_document_filter={"field_name": None, "field_value": None}
                                       ):
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
        return list(self.collection.aggregate(pipeline))[0][nested_array][0]

    def get_field_values_from_nested_array(self, collection_field_name, array_field_name, filter={}):
        pipeline = [
            {"$match": filter},
            {"$unwind": f"${collection_field_name}"},
            {"$project": {f"{collection_field_name}.{array_field_name}": 1, "_id": 0}}
        ]
        result = self.collection.aggregate(pipeline)
        return [doc[collection_field_name][array_field_name] for doc in list(self.collection.aggregate(pipeline))]

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

    # MISC
    def rename_database(self, old_db_name, new_db_name):
        # Step 1: Create a dump of the old database
        call(['mongodump', '--db', old_db_name])

        # Step 2: Restore the dump to a new database
        self.client.drop_database(new_db_name)
        call(['mongorestore', '--db', new_db_name, 'dump/' + old_db_name])

        # Step 3: (Optional) Drop the old database
        self.client.drop_database(old_db_name)
