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



fig, ax = plt.subplots()
st.session_state["geo_mx"].query("NOMEDO.isin(['D.F.', 'Mexico'])").boundary.plot(lw=1, color='grey', ax=ax)
st.session_state["geo_mpos"].query("NOMEDO.isin(['D.F.', 'Mexico'])").boundary.plot(lw=1, color='lightgrey', ax=ax, alpha=0.2)
ax.set_aspect('auto')
ax.set_axis_off()
ax.set_xticks([])
ax.set_yticks([])
fig.set_size_inches(w=20, h=10)


########################################################
st.subheader("Iztapalapa 1")
to_plot = st.session_state["df_clusters"].query("zone == 'Iztapalapa 1'")
to_plot.plot(ax=ax, color=to_plot["balanced_kmeans"], markersize=5, alpha=0.8)
l, u = (1.72e6, 1.8e6)
ax.set_xbound(lower=l, upper=u)
l, u = (2.15e6, 2.24e6)
ax.set_ybound(lower=l, upper=u)

st.pyplot(fig, use_container_width='auto')

fig.savefig("Data/Iztapalapa 1.png")

img = Image.open("Data/Iztapalapa 1.png")
st.image(img, width=1000)

########################################################

########################################################
st.subheader("Texcoco")