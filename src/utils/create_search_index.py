from elasticsearch import Elasticsearch, helpers
import os
import json
from mapping import transform_data


from dotenv import load_dotenv

load_dotenv() 


server_name=os.environ["ES_SERVER_NAME"]
server_port=os.environ["ES_SERVER_PORT"]

 
# Connexion à Elasticsearch
es = Elasticsearch(f"http://{server_name}:{server_port}")

#------------------ MAIN ---------------


data_directory = 'resources/data'  # Update this path to the directory containing your JSON files
mapping_directory = 'resources/mappings'  # Update this path to the directory containing your JSON files

# List all JSON files in the directory
data_files = [f for f in os.listdir(data_directory) if f.endswith('.json')]

# Import each JSON file into MongoDB
for data_file in data_files:
    # Extracting the filename without extension to use as collection name
    index_name = os.path.splitext(data_file)[0]
    
    # Check if the index already exists
    if es.indices.exists(index=index_name):
        # Delete the index if it exists
        es.indices.delete(index=index_name)
    
    mapping_file_path = os.path.join(mapping_directory, index_name + '.json')
    
    if os.path.exists(mapping_file_path):
        with open(mapping_file_path, 'r') as mapping_file:
            mapping = json.load(mapping_file)
            # Create the index with the mapping
            # es.indices.create(index=index_name, body=mapping, ignore=400) # ignore 400 permet d'ignorer l'erreur si l'index existe déjà
            es.indices.create(index=index_name, body=mapping)

    else:
        print(f"No mapping file found for index {index_name}. Creating index without specific mapping.")
        # Create the index without specific mapping
        es.indices.create(index=index_name)
        
    
    # Load and transform data, then insert into Elasticsearch
    with open(os.path.join(data_directory, data_file), 'r') as f:
        data = json.load(f)
        
        # Assume data is a list of documents. If not, adjust accordingly.
        transformed_data = [transform_data(doc, index_name) for doc in data]
        
        # Use the bulk API to insert transformed documents
        actions = [
            {
                "_index": index_name,
                "_source": doc,
            }
            for doc in transformed_data
        ]
        
        helpers.bulk(es, actions)

print("Data transformation and insertion complete.")

