from pymongo import MongoClient


def get_field_values_from_collection(collection, field_name):
    """

    :param field_name:
    :param collection:
    :return: List of field values for the field name in the collection of all documents
    """
    pipeline = [{"$project": {"_id": 0, field_name: f'${field_name}'}}]
    result = list(collection.aggregate(pipeline))
    field_values = [doc["name"] for doc in result]
    return field_values

def get_field_values_from_nested_array(collection, collection_field_name, array_field_name, filter={}):
    pipeline = [
        {"$match": filter},
        {"$unwind": f"${collection_field_name}"},
        {"$project": {f"{collection_field_name}.{array_field_name}": 1, "_id": 0}}
    ]

    return [doc[collection_field_name][array_field_name] for doc in list(collection.aggregate(pipeline))]


def get_document_from_nested_array(collection,
                                   nested_array,
                                   collection_filter={},
                                   array_document_filter={"field_name": None, "field_value": None}):
    pipeline = [
        {"$match": collection_filter},  # Match the document by its ID
        {"$project": {
            "test_activity": {
                "$filter": {
                    "input": f"${nested_array}",
                    "as": "activity",
                    "cond": {"$eq": [f"$$activity.{array_document_filter['field_name']}", array_document_filter['field_value']]}
                }
            },
            "_id": 0
        }}]

    return list(collection.aggregate(pipeline))[0][nested_array][0]