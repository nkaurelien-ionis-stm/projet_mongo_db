
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import json

from dotenv import load_dotenv

load_dotenv() 

db_name=os.environ["MONGO_DB_DATABASE"]
mongo_db_server_url = os.environ["MONGO_DB_URL"]

# Create a new client and connect to the server
client = MongoClient(mongo_db_server_url, server_api=ServerApi('1'))
db = client[db_name]  

#------------------ MAIN ---------------


directory = 'resources/data'  # Update this path to the directory containing your JSON files

# List all JSON files in the directory
files = [f for f in os.listdir(directory) if f.endswith('.json')]

# Import each JSON file into MongoDB
for file in files:
    # Extracting the filename without extension to use as collection name
    collection_name = os.path.splitext(file)[0]
    
    # Access the collection
    collection = db[collection_name]
    
    # Drop the collection if it exists
    collection.drop()
    
    # Open and load the JSON file
    with open(os.path.join(directory, file), 'r') as json_file:
        data = json.load(json_file)
        
        # Assuming each file contains an array of documents
        if isinstance(data, list):
            collection.insert_many(data)
        else:  # If the file contains a single document
            collection.insert_one(data)


# def import_into_mongodb(dataset_file: str, collection_name:str):
    
#     if collection_name in db.list_collection_names():
#         db[collection_name].drop()
    
#     collection = db[collection_name] 
  
#     with open(dataset_file, 'r') as fichier:
#         data = json.load(fichier)  # Charge les données JSON


#     # TODO importer en evitant les doublon grace a la cre  primaire
#     collection.insert_many(data)  # Insère toutes les données dans la collection

#     print(f"{len(data)} éléments ont été insérés dans MongoDB.")


# cwd = os.getcwd()
# dataset_file = os.path.join(cwd, 'resources/liste-des-gares.json')
# users_dataset_file = os.path.join(cwd, 'resources/users.json')

# # import_into_mongodb(dataset_file, 'gares_sncf')
# import_into_mongodb(users_dataset_file, 'users')