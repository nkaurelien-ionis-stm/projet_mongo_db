
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

user="ionis_dba"
password="ionis"
db_name="projet_mongo_db"
uri = f"mongodb+srv://{user}:{password}@cluster0.xifgzo8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[db_name]  
collection = db['gares_sncf'] 

#------------------ MAIN ---------------

import os
import json

cwd = os.getcwd()
dataset_file = os.path.join(cwd, 'resources/liste-des-gares.json')

with open(dataset_file, 'r') as fichier:
    data = json.load(fichier)  # Charge les données JSON


# TODO importer en evitant les doublon grace a la cre  primaire
collection.insert_many(data)  # Insère toutes les données dans la collection

print(f"{len(data)} éléments ont été insérés dans MongoDB.")
