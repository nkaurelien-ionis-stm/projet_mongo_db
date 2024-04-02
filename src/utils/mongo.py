import os
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv() 


db_name=os.environ["MONGO_DB_DATABASE"]
mongo_db_server_url = os.environ["MONGO_DB_URL"]

# Create a new client and connect to the server
client = MongoClient(mongo_db_server_url, server_api=ServerApi('1'))
db = client[db_name]

class MongoDb:

    collection_name = ""
  
    def query_by_id(self, value):
        collection = db[self.collection_name]
        document = collection.find_one({'_id': ObjectId(value)})
        return document

    def query_by_field(self, field_name, field_value):
        collection = db[self.collection_name]
        documents = list(collection.find({field_name: field_value}))
        return documents

    def query_by_ids(self,  ids):
        collection = db[self.collection_name]
        documents = list(collection.find({'id': {'$in': ids}}))
        return documents
