import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from utils.es import Search

es = Search()

es.index_name = "gares"

@st.cache_data
def get_data() -> pd.DataFrame:
    (gares, total) = es.get_all_data()
    print(gares)
    data = []

    df = pd.DataFrame(data, columns=["Libellé", "Commune", "Département", "Latitude", "Longitude"])

    if gares:
        for hit in gares:
            source = hit["_source"]
            data.append([source["libelle"], source["commune"], source["departemen"], source["geo_point_2d"]["lat"],
                         source["geo_point_2d"]["lon"]])
        if data:
            df = pd.DataFrame(data, columns=["Libellé", "Commune", "Département", "Latitude", "Longitude"])

    return (df, total)



# Titre de l'application
st.title('Recherche Géographique dans Elasticsearch')

# Formulaire de recherche géographique
with st.form(key='search_geo'):
    lat = st.number_input('Latitude', value=48.8566)  # Valeur par défaut pour Paris
    lon = st.number_input('Longitude', value=2.3522)  # Valeur par défaut pour Paris
    rayon = st.number_input('Rayon (km)', value=10)
    submit_button = st.form_submit_button(label='Rechercher')


# Placeholder pour afficher les résultats
results_placeholder = st.empty()


if submit_button:
    (gares, total) = es.geo_search(str(lat), str(lon), str(rayon)+"km")

    data = []

    for hit in gares:
        source = hit["_source"]
        data.append([source["libelle"], source["commune"], source["departemen"], source["geo_point_2d"]["lat"],
                     source["geo_point_2d"]["lon"]])

    if data:
        results_placeholder.write(
            "### Resulat de la recherche: \nNombre de gares trouvées sur {}km: {} / {} ".format(str(rayon), str(len(data)), str(total)))

        # Affichage du tableau de resultats
        df = pd.DataFrame(data, columns=["Libellé", "Commune", "Département", "Latitude", "Longitude"])
        st.table(df)

        df_lat_lon = df[["Latitude", "Longitude"]]

        # Affichage de la carte avec les résultats
        st.map(df, latitude='Latitude', longitude='Longitude')

    else:
        results_placeholder.write("Aucun résultat trouvé.")

(df, total)=get_data()
st.write(f"### Toute les gares \n {len(df)} / {total}")
# st.table(df)
AgGrid(df)