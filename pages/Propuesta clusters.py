import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import socket
import streamlit as st
import matplotlib.colors as mcolors
import requests


from datetime import datetime, timedelta, date
from plotly import graph_objs as go
from PIL import Image
from st_pages import show_pages_from_config, add_page_title, show_pages, Page
from shapely.geometry import Point


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

response = requests.get("https://raw.githubusercontent.com/ErickdeMauleon/data/main/style.css")
style_css = response.text

st.markdown(f'<style>{style_css}</style>', unsafe_allow_html=True)

if "df_clusters" not in st.session_state:
    st.session_state["df_clusters"] = pd.read_csv("Data/zip_code_lat_lon_cluster.csv", dtype={'zip_code': str})

    st.session_state["geo_mpos"] = (gpd.read_file('../Data/mapa_mexico/' if socket.gethostname() == "erick-huawei" else 'Data/mapa_mexico/')
                                    .set_index('CLAVE')
                                    .to_crs(epsg=4485)
                                    .assign(cve_ent=lambda _df: _df['CVE_EDO'].astype(int)
                                            , cve_mun=lambda _df: _df['CVE_MUNI'].astype(int)
                                            )
                                   )

    st.session_state["geo_mx"] = st.session_state["geo_mpos"].dissolve(by='CVE_EDO')

    geometry = [Point(xy) for xy in zip(st.session_state["df_clusters"].longitude, st.session_state["df_clusters"].latitude)]
    st.session_state["df_clusters"] = gpd.GeoDataFrame(st.session_state["df_clusters"], geometry=geometry)
    st.session_state["df_clusters"].set_crs(epsg=4326, inplace=True)
    st.session_state["df_clusters"] = st.session_state["df_clusters"].to_crs(st.session_state["geo_mx"].crs)

st.header("Propuesta de clusters")

boxstyle = dict(facecolor='white', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5')

fig, ax = plt.subplots(1, 2, figsize=(20, 8))

for i in range(2):
    st.session_state["geo_mx"].boundary.plot(lw=1, color='k', ax=ax[i])
    st.session_state["geo_mpos"].boundary.plot(lw=1, color='lightgrey', ax=ax[i], alpha=0.2)
    st.session_state["df_clusters"].plot(ax=ax[i]
            , color='red'
            , markersize=2
            , alpha=0.5
                 )

    ax[i].set_aspect('auto')
    if i == 0:
        l, u = (1.725e6, 1.87e6)
        ax[i].set_xbound(lower=l, upper=u)
        l, u = (2.12e6, 2.25e6)
        ax[i].set_ybound(lower=l, upper=u)
        ax[i].text(1.85e6, 2.18e6, 'Tlaxcala', fontsize=10, color='black', bbox=boxstyle, alpha=0.9)
        ax[i].text(1.79e6, 2.15e6, 'EdoMex', fontsize=10, color='black', bbox=boxstyle, alpha=0.9)
        ax[i].text(1.755e6, 2.1575e6, 'CDMX', fontsize=10, color='black', bbox=boxstyle, alpha=0.9)
        ax[i].text(1.732e6, 2.124e6, 'Morelos', fontsize=10, color='black', bbox=boxstyle, alpha=0.9)
        ax[i].text(1.85e6, 2.124e6, 'Puebla', fontsize=10, color='black', bbox=boxstyle, alpha=0.9)

    else:
        l, u = (1.225e6, 1.37e6)
        ax[i].set_xbound(lower=l, upper=u)
        l, u = (2.25e6, 2.38e6)
        ax[i].set_ybound(lower=l, upper=u)
        ax[i].text(1.23e6, 2.255e6, 'Guadalajara', fontsize=10, color='black', bbox=boxstyle, alpha=0.9)

    ax[i].set_xticks([])
    ax[i].set_yticks([])

st.pyplot(fig, use_container_width=True)