import os
import csv
import numpy as np
import pandas as pd
import pydeck as pdk
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

@st.cache
def generate_colors(nr_colors):
    colors = {}
    for i in range(nr_colors):
        colors[i] = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

    return colors

# @st.cache
def get_dataframe():
    
    df = pd.read_csv('tmp_dataset/super_store_geo_v2.csv')
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
    st.set_page_config(layout="wide")
    st.markdown("# Streamlit Map and Clustering")
    # show_clustering = False

    if 'show_clustering' not in st.session_state:
        st.session_state.show_clustering = False

    if 'show_channel_mix' not in st.session_state:
        st.session_state.show_channel_mix = False

    df = get_dataframe()
    df = df.dropna()

    button_columns = st.columns(2)
    graph_columns = st.columns(2)

    with button_columns[0]:
        cluster_button = st.button("Toggle clusters")
    with button_columns[1]:
        mix_button = st.button("Toggle revenue")

    if cluster_button:
        st.session_state.show_clustering = not st.session_state.show_clustering
    if mix_button:
        st.session_state.show_channel_mix = not st.session_state.show_channel_mix

    with graph_columns[1]:
        if st.session_state.show_channel_mix:
            channel_count = df.groupby(by=['Channel']).count()[['Row ID']].rename(columns={"Row ID": "Count"}).reset_index()
            channel_count['Percentage'] = channel_count['Count'] / channel_count['Count'].sum() * 100
            channel_count['Percentage'] = channel_count['Percentage'].round(decimals=3).astype(str) + "%"

            # colors = [
            #     st.get_option('theme.primaryColor'),
            #     st.get_option('theme.textColor')]
            # colors = ["#ff2b2b", "#0067c9"]
            colors = ["#ffaaab", "#ff2b2b"]

            base = alt.Chart(channel_count).encode(
                    theta=alt.Theta(field='Count', type='quantitative'),
                    color=alt.Color(field='Channel', type='nominal')
                )

            pie_chart = base.mark_arc(outerRadius=120)
            pie_text = base.mark_text(radius=180, size=25).encode(text="Percentage:N")

            combined_chart = alt.layer(
                pie_chart, pie_text
            ).configure_title(
                fontSize=24
            ).configure_range(
                category=alt.RangeScheme(colors)
            )

            st.markdown('## Revenue Channel Mix')
            st.altair_chart(combined_chart, use_container_width=True)

            historical_data = df.groupby('Order Date')[['Sales']].sum().reset_index(drop=False)
            historical_data['Order Date'] = pd.to_datetime(historical_data['Order Date'], format="%d/%m/%Y")
            historical_data = historical_data.set_index('Order Date')
            historical_data = historical_data.groupby([historical_data.index.year, historical_data.index.month]).sum().reset_index(0).rename(columns={'Order Date': 'Order Year'})
            historical_data = historical_data.reset_index(0).rename(columns={"Order Date":"Order Month"})
            historical_data_pivot = historical_data.pivot(index='Order Month', columns='Order Year')
            historical_data_pivot.columns = historical_data_pivot.columns.droplevel(0)

            st.markdown("## Historical Profitability")
            st.line_chart(historical_data_pivot)
            

    with graph_columns[0]:
        if st.session_state.show_clustering:
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
