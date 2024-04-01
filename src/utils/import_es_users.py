from elasticsearch import Elasticsearch
import json
import os
from dotenv import load_dotenv

load_dotenv() 

server_name="18.199.81.38"
db_name="users"

 
# Connexion à Elasticsearch
es = Elasticsearch(f"http://{server_name}:9200")



cwd = os.getcwd()
dataset_file = os.path.join(cwd, 'resources/users.json')

# Lire le fichier JSON
with open(dataset_file, 'r') as fichier:
    data = json.load(fichier)

mapping = {
    "mappings": {
        "properties": {
            "id":  {"type": "long"},
            "name":  {"type": "text"},
            "username":  {"type": "text"},
            "email":  {"type": "text"},
            "address":  {"type": "text"},
            "geo_point_2d":  {"type": "geo_point"},
        }
    }
}

# Créer l'index avec le mapping
es.indices.create(index=db_name, body=mapping, ignore=400)  # ignore 400 permet d'ignorer l'erreur si l'index existe déjà

# print(data)
for item in data:

    try:

        # Transformer et importer les données
        document = {
            # "id": item["id"],
            "name": item["name"],
            "username": item["username"],
            "address": "{}, {} {}".format(item["address"]["street"], item["address"]["zipcode"], item["address"]["city"]),
            "geo_point_2d": {"lat": item["address"]["geo"]["lat"], "lon": item["address"]["geo"]["lng"]}
        }
        es.index(index=db_name+'_arc', document=document)
    
        print('succes')
    except Exception as e:
        print(f"Erreur': {e}")