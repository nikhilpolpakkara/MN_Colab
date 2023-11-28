import streamlit as st

from pymongo import MongoClient

# Connect to the local MongoDB server (you can replace this with your connection string)
client = MongoClient("mongodb://localhost:27017/")

# Access a specific database (it will be created if it doesn't exist)
db = client["common"]
collections = db["department_details"]
department_details = db["department_details"].find_one()
department_details = db["department_details"]
# dept_list = list(department_details.keys())[1:]

department_details.pop("_id")

lis = []
for ta in department_details["test_activity"]:
    lis.append(department_details["test_activity"][ta]["name"])

print(lis)
durability = department_details.find({"name":"durability"})
for d in durability:
    # print(d)
    print(d['test_activity']['ta1']['name'])

# Define the aggregation pipeline
pipeline = [
    {"$match": {"name": "durability"}},
    {"$unwind": "$test_activity"},
    {"$match": {"name": "tyre_wear"}}
    # {"$project": {"test_activity.name": 1, , "_id": 0}}
]

# Execute the aggregation pipeline
result = list(collections.aggregate(pipeline))

# Print the result
for doc in result:
    # print(doc)
    # print(doc.test_activity)
    print(doc['test_activity']['test_data']['itr']['basic_details'])

pipeline = [
    {"$match": {"name": "durability"}},  # Match the document by its ID
    {"$project": {
        "test_activity": {
            "$filter": {
                "input": "$test_activity",
                "as": "activity",
                "cond": {"$eq": ["$$activity.name", "tyre wear"]}
            }
        },
        "_id": 0
    }}
]

# Execute the aggregation pipeline
result = list(collections.aggregate(pipeline))[0]['test_activity'][0]

result['test_data']['itr']['basic_details']
