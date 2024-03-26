from elasticsearch import Elasticsearch
import json
import os

server_name="18.199.81.38"
db_name="gares-voyageurs-sncf"

 
# Connexion à Elasticsearch
es = Elasticsearch(f"http://{server_name}:9200")


cwd = os.getcwd()
dataset_file = os.path.join(cwd, 'resources/liste-des-gares.json')

# Lire le fichier JSON
with open(dataset_file, 'r') as fichier:
    data = json.load(fichier)

# print(data)
for item in data:

    try:

        # Transformer et importer les données
        document = {
            "libelle": item["libelle"],
            "commune": item["commune"],
            "departemen": item["departemen"],
            "geo_point_2d": {"lat": item["geo_point_2d"]["lat"], "lon": item["geo_point_2d"]["lon"]}
        }
        es.index(index=db_name+'_arc', document=document)
    
        print('succes')
    except Exception as e:
        print(f"Erreur': {e}")