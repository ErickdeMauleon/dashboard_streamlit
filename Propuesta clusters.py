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
        Page("pages/PnL por analista.py", "PnL por analista 2", ""),
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