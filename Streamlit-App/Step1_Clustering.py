import os
import csv
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

from sklearn.cluster import KMeans

@st.cache
def generate_colors(nr_colors):
    colors = {}
    for i in range(nr_colors):
        colors[i] = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

    return colors

# @st.cache
def get_dataframe():
    
    df = pd.read_csv('tmp_dataset/super_store_geo.csv')
    df['lat'] = pd.to_numeric(df['lat'])
    df['lon'] = pd.to_numeric(df['lon'])

    return df

@st.cache
def cluster_data(df: pd.DataFrame, nr_clusters: int = 7, nr_cities: int = 10, features=["City", "Category", "Sales", "Ship Mode"], weighted_feature="None"):
    top_cities = df['City'].value_counts()[:nr_cities].keys()
    sample_df = df[df['City'].isin(top_cities)].reset_index(drop=True)

    partial_df = sample_df[features]
    dummy_df = pd.get_dummies(partial_df, columns=["City", "Category", "Ship Mode"])

    if weighted_feature != "None":
        selected_cols = [col for col in dummy_df.columns if 'City' in col]

        dummy_df[selected_cols] = dummy_df[selected_cols] * 3
    
    kmeans = KMeans(nr_clusters, init='k-means++', n_init=20)
    clusters = kmeans.fit_predict(dummy_df)
    labels = pd.DataFrame(clusters)
    labeled_orders = pd.concat((partial_df,labels),axis=1)
    labeled_orders = labeled_orders.rename({0:'labels'},axis=1)

    labeled_orders = pd.concat((sample_df[['Customer Name', 'lat', 'lon']], labeled_orders), axis=1)

    return labeled_orders


def plot_map_clusters(df):
    cluster_labels = np.sort(df['labels'].unique())
    colors = generate_colors(len(cluster_labels))

    layers = []

    for label in cluster_labels:
        data = df[df['labels'] == label][['lat', 'lon']]

        radius = 30000 - int(label)*2000

        layers.append(
            pdk.Layer(
                'ScatterplotLayer',
                data=data,
                auto_highlight=True,
                get_position='[lon, lat]',
                get_color=colors[label],
                get_radius=radius,
            ),
        )

    return layers


if __name__ == "__main__":
    st.markdown("# Streamlit Map and Clustering")

    df = get_dataframe()
    df = df.dropna()

    nr_clusters = st.slider("Number of clusters", 1, 100, 10)

    cluster_features = ["City", "Category", "Sales", "Ship Mode"]

    options = np.insert(cluster_features, 0, "None")
    weighted_feature = st.selectbox("Weighted feature", options)

    cluster_df = cluster_data(df, nr_clusters=nr_clusters, nr_cities=1000, features=cluster_features, weighted_feature=weighted_feature)
    layers = plot_map_clusters(cluster_df)
    # print(cluster_df)

    xlsx_cluster_data = st.file_uploader("Import Excel Clusters")

    st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.0902,
        longitude=-98.0,
        zoom=3.2,
        pitch=0,
    ),
    layers=layers))
    
    export_xcel_button = st.button("Export to Excel")

    if export_xcel_button:
        cluster_df.to_excel("excel_cluster_data.xlsx")
