
# INSTALL
Install python virtual env

```console
pip install --upgrade pip
sudo apt install python3-virtualenv
pip install --upgrade virtualenv
```

# Create virtual Env
Install python lib

```shell
virtualenv -p python3 venv
chmod +x venv/bin/activate
```
Install python lib
```shell
pip install -r requirements.txt
```

# RUN
Activate python venv
```shell
source ./venv/bin/activate
```

### Import dataset to mongoDb 
```shell
python src/utils/import_mongodb.py 
```

### Import dataset to Elasticseacrh 
```shell
python src/utils/create_search_index.py
```

# Run app
```shell
yarn start
# or
streamlit run src/streamlitappuser.py
```

