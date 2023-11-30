from pymongo import MongoClient

# Replace with actual credentials and details
username = 'mohit'
password = '12345'
host = '127.0.0.1'
port = '27017'

uri = f"mongodb://{username}:{password}@{host}:{port}/"

client = MongoClient(uri)

db = client["common"]
collections = db["department_details"]
department_details = db["department_details"].find_one()