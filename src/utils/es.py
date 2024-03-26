from elasticsearch import Elasticsearch

server_name = "18.199.81.38"
server_port = "9200"
index_name = "gares-voyageurs-sncf"

# Connexion à Elasticsearch
es = Elasticsearch(f"http://{server_name}:{server_port}")

class Search:

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
    resultats = es.search(index=index_name, body=requete)

    # Affichage des résultats
    # print("Nombre de gares trouvées:", resultats['hits']['total']['value'])
    for gare in resultats['hits']['hits']:
      print(gare["_source"]["libelle"], "à", rayon, "km")

    return (resultats['hits']['hits'], resultats['hits']['total']['value'])

  def get_all_data(self):
    requete = {
      "size": 100,
      "query": {
        "match_all": {}
      }
    }
    resultats = es.search(index=index_name, body=requete)

    return (resultats['hits']['hits'], resultats['hits']['total']['value'])


  def insert_documents(self, documents):
    operations = []
    for document in documents:
      operations.append({'index': {'_index': 'my_documents'}})
      operations.append(document)
    return self.es.bulk(operations=operations)

  def reindex(self):
    self.create_index()
    with open('data.json', 'rt') as f:
      documents = json.loads(f.read())
    return self.insert_documents(documents)
