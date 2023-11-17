import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import socket
import streamlit as st
import matplotlib.colors as mcolors
import requests

from shapely.geometry import Point, Polygon, MultiPolygon
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




def define_color(row):
    lights = ["lightblue", "lightgoldenrodyellow", "lightgreen", "lightcoral"]
    colors = ["blue", "gold", "green", "red"]
    darks = ["darkblue", "darkgoldenrod", "darkgreen", "darkred"]
    all_colors = [lights, colors, darks]
    _i = colors.index(row['balanced_kmeans'])
    return all_colors[int(row['subzone'] % 3)][_i]






# if "mapa_mexico" not in st.session_state:
    # Read the file https://raw.githubusercontent.com/ErickdeMauleon/data/main/colonias.csv

colonias = (pd.read_csv("https://raw.githubusercontent.com/ErickdeMauleon/data/main/colonias.csv"
                        , usecols=["codigo_postal", "latitud", "longitud"]
                        , dtype={"codigo_postal": str}
                        )
            .query("longitud.notna()")
            .query("not ((latitud > 33 or latitud < 14.5) or (longitud < -120 or longitud > -85))")
            .drop_duplicates(subset=["codigo_postal"], keep="first")
            .rename(columns={"codigo_postal": "zip_code"})
        )
colonias["zip_code"] = colonias["zip_code"].astype(str).str.zfill(5)

colonias.loc[colonias.zip_code == "54836", "latitud"] = 19.750491281899762
colonias.loc[colonias.zip_code == "54836", "longitud"] = -99.13586786079166
colonias.loc[colonias.zip_code == "72833", "latitud"] = 19.026484322916463
colonias.loc[colonias.zip_code == "72833", "longitud"] = -98.23048397597348
colonias.loc[colonias.zip_code == "54835", "latitud"] = 19.734124247119166
colonias.loc[colonias.zip_code == "54835", "longitud"] = -99.14287794033385
colonias.loc[colonias.zip_code == "72584", "latitud"] = 18.98110589884785
colonias.loc[colonias.zip_code == "72584", "longitud"] = -98.21078691265713
colonias.loc[colonias.zip_code == "54615", "latitud"] = 19.753706729044673
colonias.loc[colonias.zip_code == "54615", "longitud"] = -99.22157716494995
colonias.loc[colonias.zip_code == "72364", "latitud"] = 19.01675297246618
colonias.loc[colonias.zip_code == "72364", "longitud"] = -98.12805457729263
colonias.loc[colonias.zip_code == "72837", "latitud"] = 19.04520112863071
colonias.loc[colonias.zip_code == "72837", "longitud"] = -98.25549337513773
colonias.loc[colonias.zip_code == "72835", "latitud"] = 19.0257358819638
colonias.loc[colonias.zip_code == "72835", "longitud"] = -98.24598662855523
colonias.loc[colonias.zip_code == "45274", "latitud"] = 20.97234681173222
colonias.loc[colonias.zip_code == "45274", "longitud"] = -103.16794118010087
colonias.loc[colonias.zip_code == "47957", "latitud"] = 20.614086827961515
colonias.loc[colonias.zip_code == "47957", "longitud"] = -102.26113991885795
colonias.loc[colonias.zip_code == "45353", "latitud"] = 20.771626918778
colonias.loc[colonias.zip_code == "45353", "longitud"] = -103.67060155617497
colonias.loc[colonias.zip_code == "49016", "latitud"] = 19.72722162488196
colonias.loc[colonias.zip_code == "49016", "longitud"] = -103.46393813499246
colonias.loc[colonias.zip_code == "49106", "latitud"] = 19.653780377246846
colonias.loc[colonias.zip_code == "49106", "longitud"] = -103.50556825272699
colonias.loc[colonias.zip_code == "48634", "latitud"] = 20.09914132209491
colonias.loc[colonias.zip_code == "48634", "longitud"] = -103.97281757983387
colonias.loc[colonias.zip_code == "48428", "latitud"] = 20.334891621005077
colonias.loc[colonias.zip_code == "48428", "longitud"] = -105.34177167341775

creditos = (pd.read_csv("Data/creditos.csv"
                        , dtype={"zip_code": str})
            .merge(colonias, on="zip_code", how="left")
            )
creditos = creditos[creditos.zone.isin(["Texcoco", "Nezahualcoyotl", "Iztapalapa 1", "Cuautitlan", "Puebla"])]

mpos = (gpd.read_file('Data/mapa_mexico/')
        .set_index('CLAVE')
        .to_crs(epsg=4485)
    )
mx = mpos.dissolve(by='CVE_EDO')

# Geometry for colonias
geometry = [Point(xy) for xy in zip(colonias.longitud, colonias.latitud)]
colonias = gpd.GeoDataFrame(colonias, geometry=geometry)
colonias.set_crs(epsg=4326, inplace=True)

# Geometry for creditos
geometry = [Point(xy) for xy in zip(creditos.longitud, creditos.latitud)]
creditos = gpd.GeoDataFrame(creditos, geometry=geometry)
creditos.set_crs(epsg=4326, inplace=True)

mx = mx.to_crs(epsg=4326)
mpos = mpos.to_crs(epsg=4326)


poligonos = gpd.read_file("Data/poligonos/poligonos.shp")

st.session_state["mapa_mexico"] = 1
    



st.markdown("Así se distribuyen los créditos el día de hoy")


fig, ax = plt.subplots(1, 2, figsize=(20, 15))
for i in [0,1]:
    zonas = ("Texcoco", "Nezahualcoyotl", "Iztapalapa 1", "Cuautitlan") if i == 0 else ("Puebla", "")
    colores = ("red", "blue", "green", "orange") if i == 0 else ("purple", "")
    for _zona, _color in zip(zonas, colores):
        x = (creditos
            .query("zone == '%s'" % _zona)
            )
        if len(x) > 0:
            x.plot(ax=ax[i]
                    , color=_color
                    , markersize=10
                    , label=_zona
                )
        
    permitidos = "NOMEDO.isin(['D.F.', 'Mexico', 'Puebla', 'Tlaxcala', 'Jalisco'])"
    mpos.query(permitidos).boundary.plot(lw=1, color='lightgrey', ax=ax[i], alpha=0.4)
    mx.query(permitidos).boundary.plot(lw=1, color='k', ax=ax[i])
    l, u = (-99.5, -98.6) if i == 0 else (-98.4, -98)
    ax[i].set_xbound(lower=l, upper=u)
    l, u = (19, 20) if i == 0 else (18.9, 19.3)
    ax[i].set_ybound(lower=l, upper=u)
    ax[i].legend(fontsize=10)

# Make marker bigger in legend box
leg = ax[0].get_legend()
leg.legendHandles[0]._sizes = [100]
leg.legendHandles[1]._sizes = [100]
leg.legendHandles[2]._sizes = [100]
leg.legendHandles[3]._sizes = [100]
# Set legend box position in upper left corner
# leg.set_bbox_to_anchor((0.1, 0.9))

leg = ax[1].get_legend()
leg.legendHandles[0]._sizes = [100]

st.pyplot(fig, use_container_width=True, clear_figure=True)

st.markdown("Está es la región que vamos a delimitar")

fig, ax = plt.subplots(1, 2, figsize=(20, 15))



for i in [0,1]:
    zonas = ("Texcoco", "Nezahualcoyotl", "Iztapalapa 1", "Cuautitlan") if i == 0 else ("Puebla", "")
    colores = ("red", "blue", "green", "orange") if i == 0 else ("purple", "")
    for _zona, _color in zip(zonas, colores):
        poligono = (poligonos
                    .query("zona == '%s'" % _zona.replace(" ", "_"))
                    )
        if len(poligono) > 0:
            poligono.plot(ax=ax[i]
                    , color=_color
                    , alpha=0.3
                    , label=_zona
                )
            
        x = (creditos
            .query("zone == '%s'" % _zona)
            )
        if len(x) > 0:
            x.plot(ax=ax[i]
                    , color=_color
                    , markersize=10
                    , label=_zona
                )
        
    permitidos = "NOMEDO.isin(['D.F.', 'Mexico', 'Puebla', 'Tlaxcala'])"
    mpos.query(permitidos).boundary.plot(lw=1, color='lightgrey', ax=ax[i], alpha=0.4)
    mx.query(permitidos).boundary.plot(lw=1, color='k', ax=ax[i])
    poligonos.plot(ax=ax[i], color="lightgrey", alpha=0.5)
    l, u = (-99.5, -98.6) if i == 0 else (-98.4, -98)
    ax[i].set_xbound(lower=l, upper=u)
    l, u = (19, 20) if i == 0 else (18.9, 19.3)
    ax[i].set_ybound(lower=l, upper=u)
    ax[i].legend(fontsize=10)

# Make marker bigger in legend box
leg = ax[0].get_legend()
leg.legendHandles[0]._sizes = [100]
leg.legendHandles[1]._sizes = [100]
leg.legendHandles[2]._sizes = [100]
leg.legendHandles[3]._sizes = [100]
# Set legend box position in upper left corner
# leg.set_bbox_to_anchor((0.1, 0.9))

leg = ax[1].get_legend()
leg.legendHandles[0]._sizes = [100]

st.pyplot(fig, use_container_width=True, clear_figure=True)

poligonos_union = poligonos.assign(empresa="Yo Fio").dissolve(by="empresa")

x0 = (creditos
    .assign(dentro_zona = lambda x: x.within(poligonos_union.geometry.iloc[0]))
    .query("dentro_zona == False")
    .groupby("zone", as_index=False)
    .agg(Cuentas = ('balance', 'count')
        , balance = ('balance', 'sum')
        )
    .rename(columns={"zone": "Zona", "Cuentas": "Cuentas fuera", "balance": "Saldo capital fuera"})
    )
st.write(len(x0))
st.markdown("Estos son los créditos que están fuera de la zona")
st.dataframe(x0, height=500)

colonias["zona"] = "Fuera de zona"

fig, ax = plt.subplots(1, 2, figsize=(20, 15))

for i in [0,1]:
    zonas = ("Texcoco", "Nezahualcoyotl", "Iztapalapa 1", "Cuautitlan") if i == 0 else ("Puebla", "")
    colores = ("red", "blue", "green", "orange") if i == 0 else ("purple", "")
    for _zona, _color in zip(zonas, colores):
        poligono = (poligonos
                    .query("zona == '%s'" % _zona.replace(" ", "_"))
                    )
        if len(poligono) > 0:
            poligono.plot(ax=ax[i]
                    , color=_color
                    , alpha=0.3
                    , label=_zona
                )
            colonias.loc[colonias.within(poligono.dissolve(by="zona").geometry.iloc[0]), "zona"] = _zona

    for _zona, _color in zip(zonas, colores):
        colonias.query("zona == '%s'" % _zona).plot(ax=ax[i], color=_color, alpha=1, markersize=10, label=_zona)

    colonias.query("zona == 'Fuera de zona'").plot(ax=ax[i], color="lightgrey", alpha=0.35, markersize=10, label="Fuera de zona")
            

        
    permitidos = "NOMEDO.isin(['D.F.', 'Mexico', 'Puebla', 'Tlaxcala'])"
    mpos.query(permitidos).boundary.plot(lw=1, color='lightgrey', ax=ax[i], alpha=0.4)
    mx.query(permitidos).boundary.plot(lw=1, color='k', ax=ax[i])
    poligonos.plot(ax=ax[i], color="lightgrey", alpha=0.5)
    l, u = (-99.5, -98.6) if i == 0 else (-98.4, -98)
    ax[i].set_xbound(lower=l, upper=u)
    l, u = (19, 20) if i == 0 else (18.9, 19.3)
    ax[i].set_ybound(lower=l, upper=u)
    ax[i].legend(fontsize=10)

# Make marker bigger in legend box
leg = ax[0].get_legend()
leg.legendHandles[0]._sizes = [100]
leg.legendHandles[1]._sizes = [100]
leg.legendHandles[2]._sizes = [100]
leg.legendHandles[3]._sizes = [100]
# Set legend box position in upper right corner
leg.set_bbox_to_anchor((0.85, 1))


leg = ax[1].get_legend()
leg.legendHandles[0]._sizes = [100]

st.pyplot(fig, use_container_width=True, clear_figure=True)

x1 = (colonias
    .filter(["zip_code", "latitud", "longitud", "zona"])
    .merge(pd.read_csv("https://raw.githubusercontent.com/ErickdeMauleon/data/main/Sepomex.csv"
                        , usecols=["d_codigo", "D_mnpio", "d_estado"]
                        , dtype={"d_codigo": str}
                        )
            .drop_duplicates(subset=["d_codigo"], keep="first")
            .rename(columns={"d_codigo": "zip_code", "D_mnpio": "municipio", "d_estado": "estado"})
            , on="zip_code"
            )
    )


st.markdown("Estos son los créditos que están fuera de la zona o dentro de la zona")


csv = x1.to_csv(index=False).encode('utf-8')

_, _, _, d = st.columns(4)
d.download_button(
    label="Descargar CSV",
    data=csv,
    file_name='codigos.csv',
    mime='text/csv',
)
st.dataframe(x1.head(15), height=500)




