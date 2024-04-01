from elasticsearch import Elasticsearch
import os
import json
from dotenv import load_dotenv

load_dotenv() 


server_name=os.environ["ES_SERVER_NAME"]
server_port=os.environ["ES_SERVER_PORT"]


# Connexion à Elasticsearch
es = Elasticsearch(f"http://{server_name}:{server_port}")

class Search:

  index_name = ""

  def geo_search(self, lat: str, lng: str, rayon: str):
    # Définition du point central de recherche et du rayon
    point_central = {"lat": lat, "lon": lng}  # Exemple: Paris

    # Construction de la requête
    requete = {
      "size": 20,
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_distance": {
              "distance": rayon or "10km",
              "geo_point_2d": point_central
            }
          }
        }
      }
    }

    # Exécution de la requête dans l'index spécifié
    resultats = es.search(index=self.index_name, body=requete)

    return (resultats['hits']['hits'], resultats['hits']['total']['value'])

  def get_all_data(self):
    requete = {
      "size": 100,
      "query": {
        "match_all": {}
      }
    }
    resultats = es.search(index=self.index_name, body=requete)

    return (resultats['hits']['hits'], resultats['hits']['total']['value'])


  def insert_documents(self, documents):
    operations = []
    for document in documents:
      operations.append({'index': {'_index': self.index_name}})
      operations.append(document)
    return self.es.bulk(operations=operations)

  # def reindex(self, data_file):
  #   self.create_index()
  #   with open(data_file, 'rt') as f:
  #     documents = json.loads(f.read())
  #   return self.insert_documents(documents)
