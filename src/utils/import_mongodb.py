
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import json

user=os.environ['MONGO_DB_USER']
password=os.environ['MONGO_DB_PASSWORD']
db_name=os.environ["MONGO_DB_DATABASE"]
mongo_db_server_url = f"mongodb+srv://{user}:{password}@cluster0.xifgzo8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(mongo_db_server_url, server_api=ServerApi('1'))
db = client[db_name]  

#------------------ MAIN ---------------


def import_into_mongodb(dataset_file: str, collection_name:str):
    
    if collection_name in db.list_collection_names():
        db[collection_name].drop()
    
    collection = db[collection_name] 
  
    with open(dataset_file, 'r') as fichier:
        data = json.load(fichier)  # Charge les données JSON


    # TODO importer en evitant les doublon grace a la cre  primaire
    collection.insert_many(data)  # Insère toutes les données dans la collection

    print(f"{len(data)} éléments ont été insérés dans MongoDB.")


cwd = os.getcwd()
dataset_file = os.path.join(cwd, 'resources/liste-des-gares.json')
users_dataset_file = os.path.join(cwd, 'resources/users.json')

# import_into_mongodb(dataset_file, 'gares_sncf')
import_into_mongodb(users_dataset_file, 'users')