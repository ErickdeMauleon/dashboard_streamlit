import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import geopandas as gpd
import plotly.express as px
import socket
import streamlit as st
import matplotlib.colors as mcolors
import requests


from datetime import datetime, timedelta, date
from plotly import graph_objs as go
from PIL import Image
from st_pages import show_pages_from_config, add_page_title, show_pages, Page
# from shapely.geometry import Point


colors = plt.cm.get_cmap('Reds', 12)(range(12))
colors = list(colors)
colors.append('#3a0000')
colors.append('#000000')

url = "https://v.fastcdn.co/u/c2e5d077/58473217-0-Logo.png"
img = Image.open(requests.get(url, stream=True).raw)
show_pages_from_config()

st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title="Propuesta Zonas", page_icon=img )

show_pages(
    [
        Page("streamlit_app_web.py", "KPIS de riesgo", ""),
        Page("pages/PnL por analista.py", "PnL por analista", ""),
        Page("pages/Propuesta clusters.py", "Propuesta clusters", "")
    ])

style_css = """
body {
  background-color:rgb(255,255,255);
  
}

[data-testid="stSidebar"] {
                background-image: url(https://v.fastcdn.co/u/c2e5d077/58473217-0-Logo.png);
                background-size: 120px;
                background-repeat: no-repeat;
                background-position: 20px 20px;
            }
"""

st.markdown(f'<style>{style_css}</style>', unsafe_allow_html=True)

if "df_clusters" not in st.session_state:
    st.session_state["df_clusters"] = pd.read_csv("Data/zip_code_lat_lon_cluster.csv", dtype={'zip_code': str})

    st.session_state["all_zip_codes"] = (pd.read_csv("Data/all_zip_codes.csv", dtype={'codigo_postal': str})
                                         .rename(columns={'codigo_postal': 'zip_code'
                                                          , 'latitud': 'latitude'
                                                          , 'longitud': 'longitude'
                                                          })
                                         )
    st.session_state["all_zip_codes"]["zip_code"] = st.session_state["all_zip_codes"]["zip_code"].str.zfill(5)
    st.session_state["all_zip_codes"] = st.session_state["all_zip_codes"][st.session_state["all_zip_codes"]["zip_code"].isin(st.session_state["df_clusters"]["zip_code"]) == False]
    st.session_state["df_clusters"] = (pd.concat([st.session_state["df_clusters"], st.session_state["all_zip_codes"]], ignore_index=True)
                                       .fillna({"Cuentas": 0})
                                      )

    # st.session_state["geo_mpos"] = (gpd.read_file('../Data/mapa_mexico/' if socket.gethostname() == "erick-huawei" else 'Data/mapa_mexico/')
    #                                 .set_index('CLAVE')
    #                                 .to_crs(epsg=4485)
    #                                 .assign(cve_ent=lambda _df: _df['CVE_EDO'].astype(int)
    #                                         , cve_mun=lambda _df: _df['CVE_MUNI'].astype(int)
    #                                         )
    #                                )

    # st.session_state["geo_mx"] = st.session_state["geo_mpos"].dissolve(by='CVE_EDO')

    # geometry = [Point(xy) for xy in zip(st.session_state["df_clusters"].longitude, st.session_state["df_clusters"].latitude)]
    # st.session_state["df_clusters"] = gpd.GeoDataFrame(st.session_state["df_clusters"], geometry=geometry)
    # st.session_state["df_clusters"].set_crs(epsg=4326, inplace=True)
    # st.session_state["df_clusters"] = st.session_state["df_clusters"].to_crs(st.session_state["geo_mx"].crs)

st.header("Propuesta de clusters")


def define_color(row):
    lights = ["lightblue", "lightgoldenrodyellow", "lightgreen", "lightcoral"]
    colors = ["blue", "gold", "green", "red"]
    darks = ["darkblue", "darkgoldenrod", "darkgreen", "darkred"]
    all_colors = [lights, colors, darks]
    _i = colors.index(row['balanced_kmeans'])
    return all_colors[int(row['subzone'] % 3)][_i]
########################################################
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Iztapalapa 1", "Texcoco", "Cuautitlan", "Nezahualcoyotl", "Puebla", "Texcoco - Neza", "Descargar datos"])

colors = ["blue", "gold", "green", "red"]


with tab1:
    flag = st.checkbox("Incluir códigos postales sin clientes", value=False, key="flag_iztapalapa")
    flag2 = st.checkbox("Abrir por subzona de la subzona", value=False, key="flag_iztapalapa2")
    to_plot = st.session_state["df_clusters"].query("zone == 'Iztapalapa 1' and Cuentas > 0" if not flag else "zone == 'Iztapalapa 1'")

    if flag2:
        to_plot["balanced_kmeans"] = to_plot.apply(define_color, axis=1)
    
    fig = px.scatter_mapbox(to_plot
                            , lat="latitude"
                            , lon="longitude"
                            , color="balanced_kmeans"
                            , color_discrete_sequence=to_plot["balanced_kmeans"].unique()
                            , hover_name="zip_code"
                            , size_max=5
                            , zoom=10
                            , mapbox_style="carto-positron"
                            , height=800
                            )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(to_plot.groupby("balanced_kmeans", as_index=False).agg({"Cuentas": "sum"}))

with tab2:
    flag = st.checkbox("Incluir códigos postales sin clientes", value=False, key="flag_texcoco")
    flag2 = st.checkbox("Abrir por subzona de la subzona", value=False, key="flag_texcoco2")
    to_plot = st.session_state["df_clusters"].query("zone == 'Texcoco' and Cuentas > 0" if not flag else "zone == 'Texcoco'")
    if flag2:
        to_plot["balanced_kmeans"] = to_plot.apply(define_color, axis=1)
    
    fig = px.scatter_mapbox(to_plot
                            , lat="latitude"
                            , lon="longitude"
                            , color="balanced_kmeans"
                            , color_discrete_sequence=to_plot["balanced_kmeans"].unique()
                            , hover_name="zip_code"
                            , size_max=5
                            , zoom=10
                            , mapbox_style="carto-positron"
                            , height=800
                            )
    centroids = (st.session_state["df_clusters"]
                 .query("zone == 'Texcoco' and Cuentas > 0")
                 .groupby("balanced_kmeans", as_index=False)
                 .agg({"latitude": "mean", "longitude": "mean"})
                )
    fig.add_trace(go.Scattermapbox(
        lat=centroids["latitude"]
        , lon=centroids["longitude"]
        , mode='markers'
        , marker=go.scattermapbox.Marker(
            size=15
            , color=centroids["balanced_kmeans"]
            # , color_discrete_sequence=centroids["balanced_kmeans"].unique()
            , opacity=0.7
            , reversescale=True
            , autocolorscale=False

        )
        , text=centroids["balanced_kmeans"]
        , hoverinfo='text'
    ))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(to_plot.groupby("balanced_kmeans", as_index=False).agg({"Cuentas": "sum"}))

with tab3:
    flag = st.checkbox("Incluir códigos postales sin clientes", value=False, key="flag_cuautitlan")
    flag2 = st.checkbox("Abrir por subzona de la subzona", value=False, key="flag_cuautitlan2")
    to_plot = st.session_state["df_clusters"].query("zone == 'Cuautitlan' and Cuentas > 0" if not flag else "zone == 'Cuautitlan'")

    if flag2:
        to_plot["balanced_kmeans"] = to_plot.apply(define_color, axis=1)
    
    fig = px.scatter_mapbox(to_plot
                            , lat="latitude"
                            , lon="longitude"
                            , color="balanced_kmeans"
                            , color_discrete_sequence=to_plot["balanced_kmeans"].unique()
                            , hover_name="zip_code"
                            , size_max=5
                            , zoom=10
                            , mapbox_style="carto-positron"
                            , height=800
                            )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(to_plot.groupby("balanced_kmeans", as_index=False).agg({"Cuentas": "sum"}))

with tab4:
    flag = st.checkbox("Incluir códigos postales sin clientes", value=False, key="flag_nezahualcoyotl")
    flag2 = st.checkbox("Abrir por subzona de la subzona", value=False, key="flag_nezahualcoyotl2")
    to_plot = st.session_state["df_clusters"].query("zone == 'Nezahualcoyotl' and Cuentas > 0" if not flag else "zone == 'Nezahualcoyotl'")

    if flag2:
        to_plot["balanced_kmeans"] = to_plot.apply(define_color, axis=1)

    fig = px.scatter_mapbox(to_plot
                            , lat="latitude"
                            , lon="longitude"
                            , color="balanced_kmeans"
                            , color_discrete_sequence=to_plot["balanced_kmeans"].unique()
                            , hover_name="zip_code"
                            , size_max=5
                            , zoom=10
                            , mapbox_style="carto-positron"
                            , height=800
                            )
    centroids = (st.session_state["df_clusters"]
                 .query("zone == 'Nezahualcoyotl' and Cuentas > 0")
                 .groupby("balanced_kmeans", as_index=False)
                 .agg({"latitude": "mean", "longitude": "mean"})
                )
    fig.add_trace(go.Scattermapbox(
        lat=centroids["latitude"]
        , lon=centroids["longitude"]
        , mode='markers'
        , marker=go.scattermapbox.Marker(
            size=15
            , color=centroids["balanced_kmeans"]
            # , color_discrete_sequence=centroids["balanced_kmeans"].unique()
            , opacity=0.7
            , reversescale=True
            , autocolorscale=False

        )
        , text=centroids["balanced_kmeans"]
        , hoverinfo='text'
    ))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(to_plot.groupby("balanced_kmeans", as_index=False).agg({"Cuentas": "sum"}))

with tab5:
    flag = st.checkbox("Incluir códigos postales sin clientes", value=False, key="flag_puebla")
    flag2 = st.checkbox("Abrir por subzona de la subzona", value=False, key="flag_puebla2")
    to_plot = st.session_state["df_clusters"].query("zone == 'Puebla' and Cuentas > 0" if not flag else "zone == 'Puebla'")

    if flag2:
        to_plot["balanced_kmeans"] = to_plot.apply(define_color, axis=1)

    fig = px.scatter_mapbox(to_plot
                            , lat="latitude"
                            , lon="longitude"
                            , color="balanced_kmeans"
                            , color_discrete_sequence=to_plot["balanced_kmeans"].unique()
                            , hover_name="zip_code"
                            , size_max=5
                            , zoom=10
                            , mapbox_style="carto-positron"
                            , height=800
                            )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(to_plot.groupby("balanced_kmeans", as_index=False).agg({"Cuentas": "sum"}))

with tab6:
    flag = st.checkbox("Incluir códigos postales sin clientes", value=False, key="flag_texcoco_neza")
    flag2 = st.checkbox("Abrir por subzona de la subzona", value=False, key="flag_texcoco_neza2")
    to_plot = st.session_state["df_clusters"].query("zone.isin(['Texcoco', 'Nezahualcoyotl']) and Cuentas > 0" if not flag else "zone.isin(['Texcoco', 'Nezahualcoyotl'])")

    if flag2:
        to_plot["balanced_kmeans"] = to_plot.apply(define_color, axis=1)

    fig = px.scatter_mapbox(to_plot.query("zone == 'Nezahualcoyotl'")
                            , lat="latitude"
                            , lon="longitude"
                            , color="balanced_kmeans"
                            , color_discrete_sequence=to_plot["balanced_kmeans"].unique()
                            , hover_name="zip_code"
                            , size_max=5
                            , zoom=10
                            , mapbox_style="carto-positron"
                            , height=800
                            )
    
    # Utiliza estrellas para los puntos correspondientes a "Texcoco"
    fig.add_trace(px.Scattermapbox(
        to_plot.query("zone == 'Texcoco'")
        , lat="latitude"
        , lon="longitude"
        , color="balanced_kmeans"
        , color_discrete_sequence=to_plot["balanced_kmeans"].unique()
        , hover_name="zip_code"
        , size_max=10
        , zoom=10
        , mapbox_style="carto-positron"
        , height=800

    ).data[0])



    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(to_plot.groupby("balanced_kmeans", as_index=False).agg({"Cuentas": "sum"}))

with tab7:
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')  
    

    csv0 = convert_df(st.session_state["df_clusters"])

    st.download_button(
        label="Descargar CSV",
        data=csv0,
        file_name='all_zip_codes.csv',
        mime='text/csv',
    )
    st.dataframe(st.session_state["df_clusters"])


