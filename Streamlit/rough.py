from pymongo import MongoClient
from DBOps.crud_operations import MongoDBHandler

client = MongoClient("mongodb+srv://nikhilpolpakkara:Aspire_13@cluster0.4cun9lz.mongodb.net/?retryWrites=true&w=majority")

datahandler = MongoDBHandler(client)
datahandler.client.list_database_names()