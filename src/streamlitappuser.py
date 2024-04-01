import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from utils.es import Search

es = Search()

es.index_name = "users"

columns = ["Nom", "Username", "Adresss" , "Latitude", "Longitude" ]

start_lat=24.8918
start_lng=21.8984

@st.cache_data
def get_data() -> pd.DataFrame:
    (users, total) = es.get_all_data()
    print(users)
    data = []

    df = pd.DataFrame(data, columns=columns)

    if users:
        for hit in users:
            source = hit["_source"]
            data.append([source["name"], source["username"], source["address"], source["geo_point_2d"]["lat"],
                         source["geo_point_2d"]["lon"]])
        if data:
            df = pd.DataFrame(data, columns=columns)

    return (df, total)


# Titre de l'application
st.title('Recherche Géographique')

# Formulaire de recherche géographique
with st.form(key='search_geo'):
    lat = st.number_input('Latitude', value=start_lat)  # Valeur par défaut pour Kurtis Elwyn
    lon = st.number_input('Longitude', value=start_lng)  # Valeur par défaut pour Kurtis Elwyn
    rayon = st.number_input('Rayon (km)', value=10000)
    submit_button = st.form_submit_button(label='Rechercher')


# Placeholder pour afficher les résultats
results_placeholder = st.empty()


if submit_button:
    (users, total) = es.geo_search(str(lat), str(lon), str(rayon)+"km")

    data = []
    

    for hit in users:
        source = hit["_source"]
        data.append([source["name"], source["username"], source["address"], float(source["geo_point_2d"]["lat"]),
                        float(source["geo_point_2d"]["lon"])])
        

    if data:
        results_placeholder.write(
            "### Resultat de la recherche: \nNombre d'utilisateurs trouvées sur {}km: {} / {} ".format(str(rayon), str(len(data)), str(total)))

        # Affichage du tableau de resultats
        df = pd.DataFrame(data, columns=columns)
        st.table(df)

        df_lat_lon = df[["Latitude", "Longitude"]]

        # # Affichage de la carte avec les résultats
        st.map(df, latitude='Latitude', longitude='Longitude')
        

    else:
        results_placeholder.write("Aucun résultat trouvé.")

(df, total)=get_data()
st.write(f"### Tous les utilisateurs \n {len(df)} / {total}")
# st.table(df)
AgGrid(df)