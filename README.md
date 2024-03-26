
# INSTALL


Install python virtual env

```console
pip install --upgrade pip
sudo apt install python3-virtualenv
pip install --upgrade virtualenv
virtualenv -p python3 venv
chmod +x venv/bin/activate
```

Install python lib

```console
pip install -r src/requirements.txt
```

# RUN


Activate python venv
```console
source ./venv/bin/activate
```


### Import dataset to mongoDb 
```console
python src/utils/import_mongodb.py 
```


### Import dataset to Elasticseacrh 
```console
python src/utils/import_es.py 
```


Run app

```console
python src/main.py 
```

## generate website a partir des PDF disponibles

```console
python src/website/app.py 
```


#  prepration de la ES

#### Étape 1: 
Créer un Index avec un Mapping Géographique
Tout d'abord, vous devez créer un index dans Elasticsearch avec un mapping spécifique qui définit les champs géographiques. Elasticsearch utilise le type geo_point pour stocker des informations géographiques qui peuvent être utilisées pour des requêtes basées sur la localisation.

Vous pouvez utiliser une commande curl pour créer l'index. Par exemple:

```shell

curl -X PUT "localhost:9200/projet_mongo_db" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "libelle": { "type": "text" },
      "commune": { "type": "text" },
      "departemen": { "type": "text" },
      "geo_point_2d": { "type": "geo_point" }
    }
  }
}

```

```yaml



PUT /gares-voyageurs-sncf
{
  "mappings": {
    "properties": {
      "libelle": { "type": "text" },
      "commune": { "type": "text" },
      "departemen": { "type": "text" },
      "geo_point_2d": { "type": "geo_point" }
    }
  }
}

POST /_reindex
{
  "source": {
    "index": "projet_mongo_db_arc"
  },
  "dest": {
    "index": "gares-voyageurs-sncf"
  }
}

```# projet_mongo_db
