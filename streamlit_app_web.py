# Erick Santillan


import streamlit as st
import os
import pandas as pd
import plotly.express as px
import requests


from datetime import datetime, timedelta, date
from plotly import graph_objs as go
from PIL import Image
from st_pages import show_pages_from_config, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar


url = "https://v.fastcdn.co/u/c2e5d077/58473217-0-Logo.png"
img = Image.open(requests.get(url, stream=True).raw)
show_pages_from_config()


st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title="KPIS de riesgo", page_icon=img)
st.title("KPIS de riesgo")




def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


def prod(iterable):
    _p = 1
    for i in iterable:
        _p = _p * i
    return _p
#
# Funciones generales
#
def clean_roll(Roll):    
    if Roll == "Roll[0 to 1]":
        return "01. Roll[0 to 1]"
    if Roll == "Roll[1 to 2]":
        return "02. Roll[1 to 2]"
    if Roll == "Roll[2 to 3]":
        return "03. Roll[2 to 3]"
    if Roll == "Roll[3 to 4]":
        return "04. Roll[3 to 4]"
    if Roll == "Roll[4 to WO]":
        return "05. Roll[4 to WO]"
    if Roll == "Roll[0 to WO]" and cortes in ('Mensual', 'Todos'):
        return "06. Roll[0 to WO]"
    if Roll == "Roll anualizado" and cortes in ('Mensual', 'Todos'):
        return "07. Roll anualizado"
    if Roll == "Pérdida" and cortes in ('Mensual', 'Todos'):
        return "08. Pérdida"
    if Roll == "Pérdida (sin WO)" and cortes in ('Mensual', 'Todos'):
        return "09. Pérdida (sin WO)"
    if Roll == "Roll[4 to 5]":
        return "05. Roll[4 to 5]"
    if Roll == "Roll[5 to 6]":
        return "06. Roll[5 to 6]"
    if Roll == "Roll[6 to 7]":
        return "07. Roll[6 to 7]"
    if Roll == "Roll[7 to 8]":
        return "08. Roll[7 to 8]"
    if Roll == "Roll[8 to WO]":
        return "09. Roll[8 to WO]"
    if Roll == "Roll[0 to WO]" and cortes == 'Catorcenal':
        return "10. Roll[0 to WO]"
    if Roll == "Roll anualizado" and cortes == 'Catorcenal':
        return "11. Roll anualizado"
    if Roll == "Pérdida" and cortes == 'Catorcenal':
        return "12. Pérdida"
    if Roll == "Roll[8 to 9]":
        return "09. Roll[8 to 9]"
    if Roll == "Roll[9 to 10]":
        return "10. Roll[9 to 10]"
    if Roll == "Roll[10 to 11]":
        return "11. Roll[10 to 11]"
    if Roll == "Roll[11 to 12]":
        return "12. Roll[11 to 12]"
    if Roll == "Roll[12 to 13]":
        return "13. Roll[12 to 13]"
    if Roll == "Roll[13 to 14]":
        return "14. Roll[13 to 14]"
    if Roll == "Roll[14 to 15]":
        return "15. Roll[14 to 15]"
    if Roll == "Roll[15 to 16]":
        return "16. Roll[15 to 16]"
    if Roll == "Roll[16 to 17]":
        return "17. Roll[16 to 17]"
    if Roll == "Roll[17 to WO]":
        return "18. Roll[17 to WO]"
    if Roll == "Roll[0 to WO]" and cortes == 'Semanal':
        return "19. Roll[0 to WO]"
    if Roll == "Roll anualizado" and cortes == 'Semanal':
        return "20. Roll anualizado"
    if Roll == "Pérdida" and cortes == 'Semanal':
        return "21. Pérdida"



def get_date(i):
    return str(datetime.fromisoformat("2021-08-15")+timedelta(days=7*i))[:10]

def Bucket_Monthly(x):
    if x <= 0 :
        return '0. Bucket_Current'
    elif x >= 1 and x < 30 :
        return '1. Bucket_1_29'
    elif x >= 30 and x < 60 :
        return '2. Bucket_30_59'
    elif x >= 60 and x < 90 :
        return '3. Bucket_60_89'
    elif x >= 90 and x < 120 :
        return '4. Bucket_90_119'
    elif x >= 120 :
        return '5. Bucket_120_more'

def Bucket_Weekly(x):
    if x < 1 :
        return '0. Bucket_Current'
    elif x >= 1 and x <= 7 :
        return '01. Bucket_1_7'
    elif x >= 8 and x <= 14 :
        return '02. Bucket_8_14'
    elif x >= 15 and x <= 21 :
        return '03. Bucket_15_21'
    elif x >= 22 and x <= 28 :
        return '04. Bucket_22_28'
    elif x >= 29 and x <= 35 :
        return '05. Bucket_29_35'
    elif x >= 36 and x <= 42 :
        return '06. Bucket_36_42'
    elif x >= 43 and x <= 49 :
        return '07. Bucket_43_49'
    elif x >= 50 and x <= 56 :
        return '08. Bucket_50_56'
    elif x >= 57 and x <= 63 :
        return '09. Bucket_57_63'
    elif x >= 64 and x <= 70 :
        return '10. Bucket_64_70'
    elif x >= 71 and x <= 77 :
        return '11. Bucket_71_77'
    elif x >= 78 and x <= 84 :
        return '12. Bucket_78_84'
    elif x >= 85 and x <= 91 :
        return '13. Bucket_85_91'
    elif x >= 92 and x <= 98 :
        return '14. Bucket_92_98'
    elif x >= 99 and x <= 105 :
        return '15. Bucket_99_105'
    elif x >= 106 and x <= 112 :
        return '16. Bucket_106_112'
    elif x >= 113 and x <= 119 :
        return '17. Bucket_113_119'
    elif x >= 120 :
        return '18. Bucket_120_more'
    
def Bucket_Biweekly(x):
    if x < 1 :
        return '0. Bucket_Current'
    elif x >= 1 and x <= 15 :
        return '01. Bucket_1_15'
    elif x >= 16 and x <= 30 :
        return '02. Bucket_16_30'
    elif x >= 31 and x <= 45 :
        return '03. Bucket_31_45'
    elif x >= 46 and x <= 60 :
        return '04. Bucket_46_60'
    elif x >= 61 and x <= 75 :
        return '05. Bucket_61_75'
    elif x >= 76 and x <= 90 :
        return '06. Bucket_76_90'
    elif x >= 91 and x <= 105 :
        return '07. Bucket_91_105'
    elif x >= 106 and x <= 119 :
        return '08. Bucket_106_119'
    elif x >= 120 :
        return '09. Bucket_120_more'

def inferior(Bucket):
    if "Current" in Bucket:
        x = 0
    elif "delta" in Bucket:
        x = 120
    else:
        x = int(Bucket.split("_")[1])
    return x    

def Roll_t(i, j, mes, term_type, dataframe, flag=False):
    t = meses.index(mes)
    N = {"Mensual": 3, "Semanal": 12, "Catorcenal": 6}[cortes]
    N = min(t, N)
    
    Num = [meses[t-i] for i in range(N)]
    Den = [meses[t-i-1] for i in range(N)]
    if t-1 >= 0:
        
        n = dataframe[Num].loc[j].sum() #numerador
        d = dataframe[Den].loc[i].sum() #denominador
        
        return n/(d+int(d == 0))
    else:
        return None


def rango_lim_credito(x):
    if x <= 5000:
        return "0. Menor a $5000"
    elif x <= 15000:
        return "1. Entre $5001 y $15,0000"
    elif x <= 30000:
        return "2. Entre $15,001 y $30,0000"
    elif x <= 45000:
        return "3. Entre $30,001 y $45,0000"
    else:
        return "4. Mayor de $45,001"

def Default_rate_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    return (dataframe
            .assign(OS120 = (dataframe["Dias_de_atraso"]>=120).astype(int) * dataframe["balance"])
            .assign(balance = (dataframe["Dias_de_atraso"]<120).astype(int) * dataframe["balance"])
            .groupby(_to_group)
            .agg({"OS120": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["OS120"] / df["balance"])
            .filter(_to_group + ["Metric"])

           )

def current_pct_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Bucket.str.contains('120') == False")
            .assign(Current = dataframe["Bucket"].str.contains('Current') * dataframe["balance"])
            .groupby(_to_group)
            .agg({"Current": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["Current"] / (df["balance"] + (df["balance"] == 0).astype(int)))
            .filter(_to_group + ["Metric"])

           )


def current_sin_ip_pct_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Bucket.str.contains('120') == False")
            .assign(Current = dataframe["Bucket"].str.contains('Current') * dataframe["balance_sin_ip"])
            .groupby(_to_group)
            .agg({"Current": "sum", "balance_sin_ip": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["Current"] / (df["balance_sin_ip"] + (df["balance_sin_ip"] == 0).astype(int)))
            .filter(_to_group + ["Metric"])

           )


def os_8_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Bucket.str.contains('120') == False")
            .assign(OS8 = (dataframe["Dias_de_atraso"]>=8).astype(int) * dataframe["balance"])
            .groupby(_to_group)
            .agg({"OS8": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["OS8"] / df["balance"])
            .filter(_to_group + ["Metric"])

           )

def os_30_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Bucket.str.contains('120') == False")
            .assign(OS30 = (dataframe["Dias_de_atraso"]>=30).astype(int) * dataframe["balance"])
            .groupby(_to_group)
            .agg({"OS30": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["OS30"] / df["balance"])
            .filter(_to_group + ["Metric"])

           )

def os_60_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Bucket.str.contains('120') == False")
            .assign(OS60 = (dataframe["Dias_de_atraso"]>=60).astype(int) * dataframe["balance"])
            .groupby(_to_group)
            .agg({"OS60": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["OS60"] / df["balance"])
            .filter(_to_group + ["Metric"])

           )

def os_90_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Bucket.str.contains('120') == False")
            .assign(OS60 = (dataframe["Dias_de_atraso"]>=90).astype(int) * dataframe["balance"])
            .groupby(_to_group)
            .agg({"OS60": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["OS60"] / df["balance"])
            .filter(_to_group + ["Metric"])

           )


def coincidential_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .assign(Coincidential = ((dataframe["Dias_de_atraso"]>=120) & (dataframe["Dias_de_atraso_ant"]<120)).astype(int) * dataframe["balance"]
                , OSTotal = (dataframe["Dias_de_atraso"]<120).astype(int) * dataframe["balance"]
               )
            .groupby(_to_group)
            .agg({"Coincidential": "sum", "OSTotal": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["Coincidential"] / df["OSTotal"])
            .filter(_to_group + ["Metric"])

           )


def coincidential_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .assign(Coincidential = ((dataframe["Dias_de_atraso"]>=120) & (dataframe["Dias_de_atraso_ant"]<120)).astype(int) * dataframe["balance"]
                , OSTotal = (dataframe["Dias_de_atraso"]<120).astype(int) * dataframe["balance"]
               )
            .groupby(_to_group)
            .agg({"Coincidential": "sum", "OSTotal": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["Coincidential"] / df["OSTotal"])
            .filter(_to_group + ["Metric"])

           )

def OSTotal_sincastigos_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("balance", "sum"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def OSTotal_concastigos_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("balance", "sum"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def lagged_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    _df = (dataframe
            .assign(Coincidential = ((dataframe["Dias_de_atraso"]>=120) & (dataframe["Dias_de_atraso_ant"]<120)).astype(int) * dataframe["balance"]
                
               )
            .groupby(_to_group)
            .agg({"Coincidential": "sum"})
            .reset_index()

           )
    OS = OSTotal_sincastigos_task(dataframe, vista)

    _df = (YoFio[["Fecha_reporte"]]
            .drop_duplicates()
            .sort_values(by="Fecha_reporte", ignore_index=True)
            .merge(_df, how="left")
            .merge(OS, how="left")
            .fillna({"Coincidential": 0, "Metric": 0})
            .assign(OS_t_5 = lambda df: df["Metric"].shift(5).fillna(0))
            .assign(Metric = lambda df: df["Coincidential"] / (df["OS_t_5"]))
            .filter(_to_group + ["Metric"])
            )
    return _df


def SaldoVencido_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Status_credito=='LATE'")
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("balance", "sum"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def NumCuentas_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("ID_Credito", "nunique"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )


def Activas_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Status_credito.isin(['LATE', 'CURRENT'])")
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("ID_Credito", "nunique"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def Mora_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Status_credito.isin(['LATE'])")
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("ID_Credito", "nunique"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def reestructura_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("reestructura", "mean"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def perdida_task(dataframe, vista):
    _df = dataframe.copy()
    if vista == "":
        vista = "P"
        _df[vista] = "P"

    No_fechas = list(_df["Fecha_reporte"].unique())
    No_fechas.sort()
    No_fechas = No_fechas[:{"Mensual": 3, "Semanal": 12, "Catorcenal": 6}[cortes]]

    saldos = (_df
              .groupby(["Bucket", "Fecha_reporte", vista])
              .agg({"balance": "sum"})
              .reset_index()
             )
    t = (pd.concat([saldos
                    .query("Bucket.str.contains('120') == False")
                    , (_df
                       .query("Dias_de_atraso >= 120 and Dias_de_atraso_ant < 120")
                       .assign(Bucket = "%s. delta" % str(N+1).zfill(2 - int(N+1 < 10)))
                       .groupby(["Bucket", "Fecha_reporte", vista])
                       .agg(balance = pd.NamedAgg("balance", "sum"))
                       .reset_index()
                      )
                   ])
        )
    t = (t[[vista]]
         .drop_duplicates()
         .assign(f=1)
         .merge(t[["Bucket"]]
                .drop_duplicates()
                .assign(f=1))
         .merge(t[["Fecha_reporte"]]
                .drop_duplicates()
                .assign(f=1))
         .drop(columns=["f"])
         .merge(t
                , how="left"
               )
         .fillna({"balance":0})
         .assign(N_Bucket = lambda df: df.Bucket.apply(lambda x: int(x.split(".")[0])))
         .sort_values(by=[vista, "Bucket", "Fecha_reporte"], ignore_index=True)
        )
    _N = {"Mensual": 3, "Semanal": 12, "Catorcenal": 6}[cortes]
    t["Num"] = t.groupby([vista, "Bucket"])['balance'].rolling(window=_N, min_periods=1).sum().reset_index(drop=True)
    t["Den"] = t.groupby([vista, "Bucket"])['balance'].rolling(window=_N+1, min_periods=1).sum().reset_index(drop=True)
    t["Den"] = t["Den"] - t["balance"]

    t = (t
         .drop(columns=["balance", "Num", "Bucket"])
         .merge(t
                .drop(columns=["balance", "Den", "Bucket"])
                .assign(N_Bucket = t["N_Bucket"]-1)
                , on=[vista, "Fecha_reporte", "N_Bucket"]
               )
         .query("not Fecha_reporte.isin(%s)" % str(No_fechas))
        )

    t["Roll"] = t["Num"] / (t["Den"] + (t["Den"]==0).astype(int))

    _N = {"Mensual": 12, "Semanal": 4.5 * 12, "Todos": 12, "Catorcenal": 4.5 * 6}[cortes]
    t = (t
         .groupby(["Fecha_reporte", vista])
         .agg({"Roll": prod})
         .reset_index()
         .assign(Anualizado = lambda df: df["Roll"]* _N)
         .merge(saldos
                .query("Bucket.str.contains('Current')")
                .drop(columns=["Bucket"])
                .rename(columns={"balance": "Current"})
                , how="left"
               )
         .merge(saldos
                .groupby(["Fecha_reporte", vista])
                .agg(OS_Total = pd.NamedAgg("balance", "sum"))
                .reset_index()
                , how="left"
               )
         .assign(Metric = lambda df: df["Anualizado"]*df["Current"] / (df["OS_Total"])) # Pérdida esperada
        )
    return (t
            .filter(["Fecha_reporte", vista, "Metric"])
            )


#
# Data
#

###########################################
#  Catalogos
###########################################
cat_advisors = pd.read_csv("Data/cat_advisors.csv")
cat_municipios = pd.read_csv("Data/cat_municipios.csv")
cat_industry = pd.read_csv("Data/cat_industry.csv")

###########################################



###########################################
#  BQ
###########################################
BQ = (pd.read_csv("Data/BQ_reduced.csv")
      .merge(cat_advisors)
      .merge(cat_municipios)
      .merge(cat_industry, how="left")
      
    )
for c in ["Monto_credito", "Dias_de_atraso", "saldo", "balance"]:
    BQ[c] = BQ[c].apply(lambda x: float(x) if x!="" else 0)


BQ["Rango"] = BQ["Monto_credito"].apply(rango_lim_credito)
BQ["term_type"] = BQ["term_type"].replace({"W": "Semanal", "B": "Catorcenal", "M": "Mensual"})
BQ["Estado"] = BQ["Estado"].replace({'E': 'Edo Mex', 'C': 'CDMX', 'H': 'Hgo', 'P': 'Pue', 'J': 'Jal', 'T': 'Tlaxcala'})
BQ["Status_credito"] = BQ["Status_credito"].replace({'I': 'INACTIVE', 'C': 'CURRENT', 'A': 'APPROVED', 'L': 'LATE'})
BQ["genero_estimado"] = BQ["genero_estimado"].replace({'H': 'Hombre', '?': 'Vacio', 'M': 'Mujer'})
BQ.loc[BQ["Cartera_YoFio"] == 'C044', ["Analista"]] = "Adriana Alcantar"
BQ.loc[BQ["ZONA"] == 'Iztacalco', ["ZONA"]] = "Nezahualcoyotl"
BQ["Municipio"] = BQ["Estado"] + ", " + BQ["Municipio"]
BQ["balance_sin_ip"] = BQ["balance"].values
BQ["balance"] = BQ[["balance", "saldo"]].sum(axis=1)
BQ["Edad"] = (pd.to_datetime(BQ["Fecha_reporte"]) - pd.to_datetime(BQ["birth_date"])).dt.days / 365.25
BQ["Edad"] = BQ["Edad"].fillna(BQ["Edad"].mean()).apply(lambda x: "De %i a %i" % (int(x//5)*5, int(x//5)*5+4))
BQ["Edad"] = BQ["Edad"].replace({"De 60 a 64": "Mayor de 60"
                                 , "De 65 a 69": "Mayor de 60"
                                 , "De 70 a 74": "Mayor de 60"
                                 , "De 75 a 79": "Mayor de 60"
                                 , "De 80 a 84": "Mayor de 60"
                                 , "De 20 a 24": "De 20 a 29"
                                 , "De 25 a 29": "De 20 a 29"
                                 })


###########################################



###########################################
#  KPIS_pares
###########################################
KPIS_pares_df = pd.read_csv("Data/KPIS_pares.csv")
KPIS_pares_df["Value"] = KPIS_pares_df["Value"].apply(float)
###########################################



###########################################
#  PROMEDIOS
###########################################
PROMEDIOS_df = pd.read_csv("Data/PROMEDIOS.csv")
for c in PROMEDIOS_df.columns:
    if c not in ("Corte", "Fecha_reporte"):
        PROMEDIOS_df[c] = PROMEDIOS_df[c].apply(float) 
###########################################







##################################################################
##
## STREAMLIT APP
##
##################################################################



response = requests.get("https://raw.githubusercontent.com/ErickdeMauleon/data/main/style.css")
style_css = response.text

st.markdown(f'<style>{style_css}</style>', unsafe_allow_html=True)
#st.sidebar.image("https://v.fastcdn.co/u/c2e5d077/58473217-0-Logo.png")
#st.table(BQ.sample(5).head())
st.sidebar.header('Dashboard KPIS de riesgo')

st.sidebar.subheader('Selecciona parametros:')
_cortes = st.sidebar.selectbox('Selecciona los cierres:'
                                 , ('Por mes', 'Por quincenas', 'Por semanas')) 
cortes = {"Por quincenas": 'Catorcenal'
          , "Por mes": 'Mensual'
          , "Por semanas":  'Semanal'
         }[_cortes]



term_type = st.sidebar.multiselect('Selecciona tipo de corte de cartera'
                                 , ('Todos', 'Catorcenal', 'Mensual', 'Semanal')
                                 , default='Todos'
                                 ) 






zona_list = list(BQ.ZONA.drop_duplicates().values)
zona_list.sort()
zona = st.sidebar.multiselect('Selecciona la zona del analista'
                            , ['Todas'] + zona_list
                            , default='Todas'
                            )



Analista_list = list(BQ.Analista.dropna().drop_duplicates().values)
Analista_list.sort()
analista = st.sidebar.multiselect('Selecciona el analista'
                                  , ['Todos'] + Analista_list
                                  , default='Todos'
                                 )


Edades_list = list(BQ.Edad.drop_duplicates().values)
Edades_list.sort()
edad = st.sidebar.multiselect('Selecciona la edad del tiendero'
                            , ['Todos'] + Edades_list
                            , default='Todos'
                            )

estados_list = list(BQ.Estado.unique())
estados_list.sort()
estado = st.sidebar.multiselect('Selecciona el estado de la tienda'
                             , ['Todos'] + estados_list
                             , default='Todos'
                            )

mnpios_list = list(BQ.Municipio.unique())
mnpios_list.sort()
municipio = st.sidebar.multiselect('Selecciona el municipio de la tienda'
                                 , ['Todos'] + mnpios_list
                                 , default='Todos'
                                 )



genero = st.sidebar.multiselect('Selecciona el género del tiendero'
                                 , ["Todos", "Hombre", "Mujer", "?"]
                                 , default='Todos'
                                 )

rangos_list = list(BQ.Rango.unique())
rangos_list.sort()
rangos = st.sidebar.multiselect('Selecciona el rango del límite de credito'
                                 , ['Todos'] + rangos_list
                                 , default='Todos'
                                 )

industry_list = list(BQ.industry.unique())
industry_list.sort()
industry = st.sidebar.multiselect('Selecciona el giro del negocio'
                                 , ['Todos'] + industry_list
                                 , default='Todos'
                                 )

flag_general = ((term_type == ['Todos']) 
                & (zona == ['Todas']) 
                & (analista == ['Todos'])
                & (estado == ['Todos']) 
                & (municipio == ['Todos']) 
                & (rangos == ['Todos']) 
               )
#


filtro_dict = {'Todos': {"f2": ", ".join(["'%s'" % str(d)[:10] for d in pd.date_range("2021-03-31"
                                                                                        , periods=50
                                                                                        , freq="M")])
                         , "Bucket": Bucket_Monthly
                         , "buckets": ['0. Bucket_Current'
                                       , '1. Bucket_1_29'
                                       , '2. Bucket_30_59'
                                       , '3. Bucket_60_89'
                                       , '4. Bucket_90_119'
                                       , '5. Bucket_120_more'
                                       , '6. delta']
                         , "top_rolls": 4
                         , "term_type": "Monthly"
                        }
               , 'Catorcenal': {"f2": ", ".join(["'%s'" % get_date(i) for i in range(160) if i % 2 == 0])
                                , "Bucket": Bucket_Biweekly
                                , "buckets": ['0. Bucket_Current'
                                              , '01. Bucket_1_15'
                                              , '02. Bucket_16_30'
                                              , '03. Bucket_31_45'
                                              , '04. Bucket_46_60'
                                              , '05. Bucket_61_75'
                                              , '06. Bucket_76_90'
                                              , '07. Bucket_91_105'
                                              , '08. Bucket_106_119'
                                              , '09. Bucket_120_more'
                                              , '10. delta']
                                , "top_rolls": 8
                                , "term_type": "Biweekly"
                               }
               , 'Semanal': {"f2": ", ".join(["'%s'" % get_date(i) for i in range(160)])
                             , "Bucket": Bucket_Weekly
                             , "buckets": ['0. Bucket_Current'
                                           , '01. Bucket_1_7'
                                           , '02. Bucket_8_14'
                                           , '03. Bucket_15_21'
                                           , '04. Bucket_22_28'
                                           , '05. Bucket_29_35'
                                           , '06. Bucket_36_42'
                                           , '07. Bucket_43_49'
                                           , '08. Bucket_50_56'
                                           , '09. Bucket_57_63'
                                           , '10. Bucket_64_70'
                                           , '11. Bucket_71_77'
                                           , '12. Bucket_78_84'
                                           , '13. Bucket_85_91'
                                           , '14. Bucket_92_98'
                                           , '15. Bucket_99_105'
                                           , '16. Bucket_106_112'
                                           , '17. Bucket_113_119'
                                           , '18. Bucket_120_more'
                                           , '19. delta']
                             , "top_rolls": 17
                             , "term_type": "Weekly"
                            }
               , 'Mensual': {"f2": ", ".join(["'%s'" % str(d)[:10] for d in pd.date_range("2021-03-31"
                                                                                            , periods=50
                                                                                            , freq="M")])
                             , "Bucket": Bucket_Monthly
                             , "buckets": ['0. Bucket_Current'
                                           , '1. Bucket_1_29'
                                           , '2. Bucket_30_59'
                                           , '3. Bucket_60_89'
                                           , '4. Bucket_90_119'
                                           , '5. Bucket_120_more'
                                           , '6. delta']
                             , "top_rolls": 4
                             , "term_type": "Monthly"
                            }
              }[cortes]


if 'Todos' in term_type:
    f1 = "term_type == term_type"
else:
    f1 = " term_type.isin(%s)" % str(term_type)

f2 = filtro_dict["f2"]


if 'Todas' in zona:
    f3 = ""
else:
    f3 = " and ZONA.isin(%s)" % str(zona)
    
    
if 'Todos' in estado:
    f4 = ""
else:
    f4 = " and Estado.isin(%s)" % str(estado)
    
if 'Todos' in analista:
    f5 = ""
else:
    f5 = " and Analista.isin(%s)" % str(analista)
    
if 'Todos' in municipio:
    f6 = ""
else:
    f6 = " and Municipio.isin(%s)" % str(municipio)
    
if 'Todos' in rangos:
    f7 = ""
else:
    f7 = " and Rango.isin(%s)" % str(rangos)

if 'Todos' in genero:
    f8 = ""
else:
    f8 = " and genero_estimado.isin(%s)" % str(genero)

if 'Todos' in industry:
    f9 = ""
else:
    f9 = " and industry.isin(%s)" % str(industry)

if 'Todos' in edad:
    f10 = ""
else:
    f10 = " and Edad.isin(%s)" % str(edad)

N = filtro_dict["top_rolls"]   
 
filtro_BQ = "%s and Fecha_reporte in (%s) %s %s %s %s %s %s %s %s" % (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10)
    

YoFio = (BQ
         .query("Fecha_reporte in (%s)" % f2)
         .assign(Bucket = lambda df: df.Dias_de_atraso.apply(filtro_dict["Bucket"]))
         .sort_values(by=["ID_Credito", "Fecha_reporte"]
                         , ignore_index=True)
        )

temp = (BQ
        .query(filtro_BQ)
        .assign(Bucket = lambda df: df.Dias_de_atraso.apply(filtro_dict["Bucket"]))
        .sort_values(by=["ID_Credito", "Fecha_reporte"]
                         , ignore_index=True)
        )

if len(temp) == 0:
    st.write("No hay clientes con las condiciones que pides.")
else:
    temp["t"] = (temp
                 .assign(t=range(len(temp)))
                 .groupby(["ID_Credito"])
                 .t.rank()
                )
    temp = (temp
            .merge(temp
                   .assign(t=lambda df: df.t+1)
                   [["ID_Credito", "Dias_de_atraso", "Fecha_reporte", "t"]]
                   , on=["ID_Credito", "t"]
                   , suffixes=("", "_ant")
                   , how="left")
            .fillna({"Dias_de_atraso_ant": 0})
         )



    YoFio["t"] = (YoFio
                 .assign(t=range(len(YoFio)))
                 .groupby(["ID_Credito"])
                 .t.rank()
                )
    YoFio = (YoFio
            .merge(YoFio
                   .assign(t=lambda df: df.t+1)
                   [["ID_Credito", "Dias_de_atraso", "Fecha_reporte", "t"]]
                   , on=["ID_Credito", "t"]
                   , suffixes=("", "_ant")
                   , how="left")
            .fillna({"Dias_de_atraso_ant": 0})
         )
    
    
        
    temp_agg = (pd.concat([
        (temp
          .groupby(["Bucket", "Fecha_reporte"])
          .agg({"balance": "sum"})
          .reset_index()
          .pivot(index=["Bucket"]
                 , columns="Fecha_reporte"
                 , values="balance"
                 )
          )
        , (temp
           .query("Dias_de_atraso >= 120 and Dias_de_atraso_ant < 120")
           .assign(Bucket = "%s. delta" % str(N+2).zfill(2 - int(N+2 < 10)))
           .groupby(["Bucket", "Fecha_reporte"])
           .agg(Value = pd.NamedAgg("balance", "sum"))
           .reset_index()
           .pivot(index="Bucket"
                  , columns="Fecha_reporte"
                  , values="Value"
                  )
           )
        ])
        .fillna(0)
        )
    #st.dataframe(temp_agg)
    
    cols = list(temp_agg.columns)[::-1]
    
    temp_agg = (pd.DataFrame({"Bucket": filtro_dict["buckets"]})
                .merge(temp_agg
                       .reset_index()
                       , how="left")
                .set_index("Bucket")
                .fillna(0)
                .filter(cols)
               )
    
    
    
    
    
        
    

    
    
    
    
    
    #
    # Rolls
    #
    Roll_value = []
    Roll_desc = []
    Fecha_reporte = []
    
    meses = [c for c in temp_agg.columns if '-' in c]
    meses.sort()
    
    
    
    for m in meses[3:]:
        for i in range(N):
            j = i+1
            Roll_value.append(Roll_t(i, j, m, filtro_dict["term_type"], dataframe=temp_agg.reset_index()))
            Roll_desc.append("Roll[%i to %i]" % (i, j))
            Fecha_reporte.append(m)
                
        Roll_value.append(Roll_t(N, N+2, m, filtro_dict["term_type"], dataframe=temp_agg.reset_index()))
        Roll_desc.append("Roll[%i to WO]" % N)
        Fecha_reporte.append(m)
        
    rolls = (pd.DataFrame({"Mes": Fecha_reporte
                           , "Roll": Roll_desc
                           , "Value": Roll_value
                           })
             .dropna()
            )
    rolls = pd.concat([rolls
                       , (rolls
                          .assign(Roll = "Roll[0 to WO]")
                          .groupby(["Mes", "Roll"])
                          .agg({"Value": prod})
                          .reset_index()
                         )
                      ]
                      , ignore_index=True)
        
    rolls = (pd.concat([rolls
                       , rolls
                       .query("Roll == 'Roll[0 to WO]'")
                       .reset_index(drop=True)
                       .assign(Roll = 'Roll anualizado'
                               , Value = lambda df: df.Value * {"Mensual": 12
                                                                , "Semanal": 4.5 * 12
                                                                , "Todos": 12
                                                                , "Catorcenal": 4.5 * 6
                                                                }[cortes]
                              )
                       [list(rolls.columns)]
                      ])
             )
    
    
    
    
    Perdida = (temp_agg
                .reset_index()
                .melt(id_vars=["Bucket"]
                      , var_name="Mes"
                      , value_name="balance"
                      )
               .query("not Bucket.str.contains('delta')", engine="python")
               .groupby(["Mes"])
               .agg(OS_Total = pd.NamedAgg("balance", "sum"))
               .reset_index()
               .merge(temp_agg
                      .reset_index()
                      .melt(id_vars=["Bucket"]
                            , var_name="Mes"
                            , value_name="balance"
                           )
                      .query("Bucket.str.contains('Current')", engine="python")
                      .rename(columns={"balance": "Current"})
                      .drop(columns="Bucket")
                     )
               .merge(rolls
                      .query("Roll == 'Roll anualizado'")
                      .reset_index(drop=True)
                      .rename(columns={"Value": "Anualizado"})
                      , how="left"
                     )
               .assign(Roll = "Pérdida"
                       , Value = lambda df: df.Anualizado*df.Current/df.OS_Total # Valor de la pérdida
                      )
               .fillna(0)
              )
    
    rolls = pd.concat([rolls, Perdida[list(rolls.columns)]])
    
    rolls["Roll"] = rolls["Roll"].apply(clean_roll)
    
    rolls_toplot = (rolls
                    .assign(Value = rolls.Value.apply(lambda x: "{:.1f}%".format(100*x)))
                    .pivot(index=["Roll"]
                           , columns=["Mes"]
                           , values="Value"
                          )
                    .fillna("0.0%")
                   )
    
    
    # Row A
    _max = temp.Fecha_reporte.max()

    st.markdown("### Tamaño cartera (fotografía al %s)" % _max)

#    _a1, _a2, _a3, _a4 = st.columns(4)
    

#    _a1.metric("Num de cuentas", "%i" % temp.query("Fecha_reporte == '%s'" % _max).shape[0])
#   _a2.metric("Líneas activas", "%i" % temp.query("Fecha_reporte == '%s' and Status_credito in ('CURRENT','LATE')" % _max).shape[0])
#   _num = temp.query("Fecha_reporte == '%s' and Status_credito in ('LATE') " % _max)["balance"].sum()
#   _a3.metric("Saldo en mora", "%s" % "{:,.2f}".format(_num))
#   _den = temp.query("Fecha_reporte == '%s'" % _max)["balance"].sum()
#   _a4.metric("Saldo", "%s" % "{:,.2f}".format(_den))
#   _aa1, _aa2, _aa3, _aa4 = st.columns(4)
#   _aa1.metric("Status current", "%i" % temp.query("Fecha_reporte == '%s' and Status_credito in ('CURRENT')" % _max).shape[0])
#   _aa2.metric("Bucket current", "%i" % temp.query("Fecha_reporte == '%s' and Dias_de_atraso < 1" % _max).shape[0])
#   _aa3.metric("Saldo mora", "%i" % temp.query("Fecha_reporte == '%s' and Dias_de_atraso >= 1" % _max)["balance"].sum())
#   _aa4.metric("% Current", "{:.1f}%".format(100*(1-_num/_den)))
    #_a5.metric("Líneas Current %", "%i" % temp.query("Fecha_reporte == '%s' and Status_credito in ('LATE')" % _max).shape[0])
    # st.dataframe(temp[["Fecha_reporte", "Tasa_interes"]]
    #              .assign(Tasa_interes = lambda _df: _df.apply(lambda row: 4*row.Tasa_interes 
    #                                                           if row.Fecha_reporte < "2023-05-02" 
    #                                                           else row.Tasa_interes
    #                                                           , axis=1))
    #               .assign(Rango = lambda _df: _df.Tasa_interes.apply(lambda x: 2*(x // 2)))
    #               .groupby(["Rango"])
    #                 .agg({"Tasa_interes": "count"})
    #                 .rename(columns={"Tasa_interes": "Num de cuentas"})
    #                 .reset_index()
    #              )

    _b1, _b2, _b3, _b4, _ = st.columns(5)
    kpi_sel_0 = _b1.selectbox("Selecciona la métrica", 
                              ["Número de cuentas"
                              , "Cuentas (sin castigo)"
                              , "Cuentas (castigadas)"
                              , "Saldo Total"
                              , "Saldo Total (sin castigos)"
                              , "Saldo Total (castigado)"
                              ])
    


    factor_sel_0 = _b2.selectbox("Selecciona la vista a desagregar", 
                                ["Por tipo de corte"
                                , "Por zona"
                                , "Por analista"
                                , "Por edad del tiendero"
                                , "Por estado de la tienda"
                                , "Por rango de crédito"
                                , "Por municipio"
                                , "Por género del tiendero"
                                , "Por giro del negocio"

                                ])
    _kpi = {"Número de cuentas": {"y": "account_id", "query": ""}
            , "Cuentas (sin castigo)": {"y": "account_id", "query": "and Dias_de_atraso < 120"}
            , "Cuentas (castigadas)": {"y": "account_id", "query": "and Dias_de_atraso >= 120"}
            , "Saldo Total": {"y": "balance", "query": ""}
            , "Saldo Total (sin castigos)": {"y": "balance", "query": "and Dias_de_atraso < 120"}
            , "Saldo Total (castigado)": {"y": "balance", "query": "and Dias_de_atraso >= 120"}
           }[kpi_sel_0]
           
    factor = {"Por tipo de corte": "term_type"
              , "Por zona": "ZONA"
              , "Por analista": "Analista"
              , "Por edad del tiendero": "Edad"
              , "Por estado de la tienda": "Estado"
              , "Por rango de crédito": "Rango"
              , "Por municipio": "Municipio"
              , "Por género del tiendero": "genero_estimado"
              , "Por giro del negocio": "industry"
             }[factor_sel_0]

    comp_sel_0 = _b3.selectbox("Selecciona la comparación", 
                                ["Valores absolutos"
                                , "Valores porcentuales"
                                ])
    sort_by = _b4.selectbox("Ordenar por:", 
                             ["Alfabéticamente"
                                , "Valor más grande"
                                ])
    flag_sort = (sort_by == "Alfabéticamente")

    
    
    _to_plot0 = (YoFio
                 .query("Fecha_reporte == '%s'" % _max)
                 .assign(account_id = 1)
                 .groupby([factor])
                 .agg({"account_id": "sum"
                       , "balance": "sum"})
                 .reset_index()
                )

    _to_plot = (temp
                .query("Fecha_reporte == '%s'" % _max)
                .assign(account_id = 1)
                .query("Fecha_reporte == '%s' %s" % (_max, _kpi["query"]))
                .groupby([factor])
                .agg({"account_id": "sum"
                        , "balance": "sum"})
                .reset_index()
               )



    if comp_sel_0 == 'Valores porcentuales':
        _to_plot["account_id"] = _to_plot["account_id"] / _to_plot["account_id"].sum()
        _to_plot["balance"] = _to_plot["balance"] / _to_plot["balance"].sum()
        _to_plot0["account_id"] = _to_plot0["account_id"] / _to_plot0["account_id"].sum()
        _to_plot0["balance"] = _to_plot0["balance"] / _to_plot0["balance"].sum()
    

    _to_plot0 = (_to_plot0
                 .merge(_to_plot
                    , how="left"
                    , on=[factor]
                    , suffixes=["_avg", ""]
                    )
                 .fillna(0)
                 .sort_values(by=[factor if flag_sort else _kpi["y"]]
                            , ascending=[flag_sort]
                                  )
                )

    #st.dataframe(_to_plot0)
    if comp_sel_0 != 'Valores porcentuales':
        fig0 = px.bar(_to_plot
                      .sort_values(by=[factor if flag_sort else _kpi["y"]]
                                   , ascending=[flag_sort]
                                  )
                     , y=_kpi["y"]
                     , x=factor
                     , labels={factor: factor_sel_0
                               , _kpi["y"]: kpi_sel_0
                              }
                    )
        if comp_sel_0 == 'Valores porcentuales':
            fig0.layout.yaxis.tickformat = ',.1%'
            fig0.layout.yaxis.range = [0, 1]
        else:
            fig0.layout.yaxis.tickformat = ',.0f'
            if _kpi["y"] == "balance":
                fig0.layout.yaxis.tickprefix = '$'
        
    else:
        fig0 = go.Figure()
        fig0.add_trace(go.Bar(x=_to_plot0[factor]
                              , y=_to_plot0[_kpi["y"]+"_avg"]
                              , name="Promedio YoFio"
                              , marker_color="lightblue"
                             )
                      )
        fig0.add_trace(go.Bar(x=_to_plot0[factor]
                              , y=_to_plot0[_kpi["y"]]
                              , width=len(_to_plot0)*[0.5]
                              , name="Cartera seleccionada"
                              , marker_color='royalblue'
                             )
                       )
        fig0.update_layout(barmode = 'overlay')
        fig0.layout.yaxis.tickformat = ',.1%'
        fig0.layout.yaxis.range = [0, 1]


    fig0.layout.xaxis.type = 'category'
    fig0.update_traces(textfont_size=12
                      , textangle=0
                      , textposition="inside"
                      , cliponaxis=False
                      )
    fig0.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')







    st.plotly_chart(fig0
                    , use_container_width=True
                    , height = 450
                    , theme="streamlit"
                    )


    st.markdown('### Cortes')
    
    csv0 = convert_df(pd.concat([temp
                                 .groupby(["Fecha_reporte"])
                                 .agg({"saldo": "sum"})
                                 .transpose()
                                 #.applymap(lambda x: "${:,.0f}".format(x))
                                 .filter(cols)
                                 .assign(Saldo="Saldo current")
                                 .rename(columns={"Saldo": "Saldo current"})
                                 .set_index("Saldo current")
                                , temp_agg]).reset_index()
    )
    _d1, _d2, _d3 = st.columns((9,2,2))
    _d1.markdown("Saldo de compra de central de abastos o a distribuidor (aún no desembolsado)")
    _d3.download_button(
        label="Descargar CSV",
        data=csv0,
        file_name='cortes.csv',
        mime='text/csv',
    )
    st.dataframe(temp
                 .groupby(["Fecha_reporte"])
                 .agg({"saldo": "sum"})
                 .transpose()
                 .applymap(lambda x: "${:,.0f}".format(x))
                 .filter(cols)
                 .assign(Saldo="Total")
                 .rename(columns={"Saldo": "Saldo current"})
                 .set_index("Saldo current")
                 , use_container_width=True)
    
    st.dataframe(temp_agg
                 .applymap(lambda x: "${:,.0f}".format(x))
                 , use_container_width=True)
    
    st.dataframe(temp_agg
                 .iloc[:N+1]
                 .sum()
                 .apply(lambda x: "${:,.0f}".format(x))
                 .to_frame()
                 .transpose()
                 .assign(i="Total")
                 .rename(columns={"i": "Saldo menor a 120 días"})
                 .set_index("Saldo menor a 120 días")
                 , use_container_width=True)
    
    st.markdown('### Métricas')
    col1, col2, _, col5 = st.columns(4)
    kpi_selected = col1.selectbox("Selecciona la métrica", 
                                  ["Current %"
                                   , "Current % (sin compras inventario o proveedor)"
                                   , "Default rate"
                                   , "OS 8 mas %"
                                   , "OS 30 mas %"
                                   , "OS 60 mas %"
                                   , "OS 90 mas %"
                                   , "Pérdida esperada"
                                   , "Coincidential WO"
                                   , "Lagged WO"
                                   , "Saldo Total (sin castigos)"
                                   , "Saldo Total (con castigos)"
                                   , "Saldo Vencido"
                                   , "Número de cuentas"
                                   , "Número de cuentas Activas"
                                   , "Número de cuentas Mora"
                                   , "Reestructuras %"
                                   ])

    vista_selected = col2.selectbox("Selecciona la vista a desagregar:", 
                                   ["-- Sin vista --"
                                    , "Por tipo de corte"
                                    , "Por zona"
                                    , "Por analista"
                                    , "Por estado de la tienda"
                                    , "Por edad del tiendero"
                                    , "Por rango de crédito"
                                    , "Por municipio"
                                    , "Por género del tiendero"
                                    , "Por giro del negocio"
                                    ])
           
    vista = {"Por tipo de corte": "term_type"
              , "Por zona": "ZONA"
              , "Por analista": "Analista"
              , "Por edad del tiendero": "Edad"
              , "Por estado de la tienda": "Estado"
              , "Por rango de crédito": "Rango"
              , "Por municipio": "Municipio"
              , "Por género del tiendero": "genero_estimado"
              , "Por giro del negocio": "industry"
              , "-- Sin vista --": ""
             }[vista_selected]
    
    kpi = {"Current %": "Current_pct" 
            , "Current % (sin compras inventario o proveedor)": "current_sin_ip_pct"
            , "Default rate": "Default"
             , "OS 8 mas %": "OS_8_pct"
             , "OS 30 mas %": "OS_30more_pct"
             , "OS 60 mas %": "OS_60more_pct"
             , "OS 90 mas %": "OS_90_more"
             , "Pérdida esperada": "Perdida"
             , "Coincidential WO": "CoincidentialWO"
             , "Lagged WO": "LaggedWO"
             , "Saldo Total (sin castigos)": "OSTotal"
             , "Saldo Total (con castigos)": "balance_castigos"
             , "Saldo Vencido": "Saldo_Vencido" 
             , "Número de cuentas": "Num_Cuentas"
             , "Número de cuentas Activas": "Activas"
             , "Número de cuentas Mora": "Mora"
             , "Reestructuras %": "reestructura"
             }[kpi_selected]

    kpi_task = {"Current %": current_pct_task 
                , "Current % (sin compras inventario o proveedor)": current_sin_ip_pct_task
                 , "Default rate": Default_rate_task
                 , "OS 8 mas %": os_8_task
                 , "OS 30 mas %": os_30_task
                 , "OS 60 mas %": os_60_task
                 , "OS 90 mas %": os_90_task
                 , "Pérdida esperada": perdida_task
                 , "Coincidential WO": coincidential_task
                 , "Lagged WO": lagged_task
                 , "Saldo Total (sin castigos)": OSTotal_sincastigos_task
                 , "Saldo Total (con castigos)": OSTotal_concastigos_task
                 , "Saldo Vencido": SaldoVencido_task 
                 , "Número de cuentas": NumCuentas_task
                 , "Número de cuentas Activas": Activas_task
                 , "Número de cuentas Mora": Mora_task
                 , "Reestructuras %": reestructura_task
                 }[kpi_selected]
    
    kpi_des = {"Current %": "Saldo en Bucket_Current dividido entre Saldo Total (sin castigos)" 
               , "Current % (sin compras inventario o proveedor)": "Saldo en Bucket_Current sin incluir saldo de compras a proveedor o inventario dividido entre Saldo Total (sin castigos)"
               , "Default rate": "Saldo a más de 120 días dividido entre Saldo Total (sin castigos)"
               , "OS 8 mas %": "Saldo a más de 8 días de atraso dividido entre Saldo Total (sin castigos)"
               , "OS 30 mas %": "Saldo a más de 30 días de atraso dividido entre Saldo Total (sin castigos)"
               , "OS 60 mas %": "Saldo a más de 60 días de atraso dividido entre Saldo Total (sin castigos)"
               , "OS 90 mas %": "Saldo a más de 90 días de atraso dividido entre Saldo Total (sin castigos)"
               , "Pérdida esperada": "Roll anualizado por saldo Current entre Saldo Total (incluyendo castigos). Valor probabilístico."
               , "Coincidential WO": "Bucket Delta dividido entre Saldo Total (sin castigos)"
               , "Lagged WO": "Bucket Delta dividido entre Saldo Total (sin castigos) de hace 5 períodos."
               , "Saldo Total (sin castigos)": "Saldo Total sin bucket 120"
               , "Saldo Vencido": "Saldo en status LATE"
               , "Saldo Total (con castigos)": "Saldo Total incluyendo bucket 120"
               , "Número de cuentas": "Total cuentas colocadas (acumuladas)"
               , "Reestructuras %": "Porcentaje de cuentas reestructuradas sin considerar castigadas."
               , "Número de cuentas Activas": "Cuentas en CURRENT o LATE"
               , "Número de cuentas Mora": "Cuentas en LATE"
              }[kpi_selected]
    
    
    if vista == "":
        Cartera = kpi_task(temp, vista).assign(Vista="Cartera seleccionada")
    else: 
        Cartera = kpi_task(temp, vista).rename(columns={vista: "Vista"})


    if False:
        last = temp[temp["Fecha_reporte"] == temp["Fecha_reporte"].max()]
        temp.columns
        _x0 = len(last)
        _x = last["balance"].sum() 
        st.write("Número de cuentas en la cartera seleccionada: ", f"{_x0:,.0f}")
        st.write("Saldo total sin incluir saldo de compras a proveedor o inventario: $", f"{_x:,.0f}")
        cuadre_robin = convert_df(last)

        st.download_button(
            label="Descargar CSV",
            data=cuadre_robin,
            file_name='Metricas.csv',
            mime='text/csv',
        )






    flag = kpi in ('Num_Cuentas', 'Activas', 'Mora', "Saldo_Vencido", "OSTotal", "balance_castigos")

    if flag:

        to_plot = pd.concat([Cartera])

        fig1 = px.line(to_plot
                        , x="Fecha_reporte"
                        , y="Metric"
                        , color="Vista"
                       )

        if kpi in ("OSTotal", "balance_castigos", "Saldo_Vencido"):
            fig1.layout.yaxis.tickformat = '$,'
        else:
            fig1.layout.yaxis.tickformat = ','
    else:
        Promedio = kpi_task(YoFio, "").assign(Vista="Promedio YoFio")
        to_plot = pd.concat([Promedio, Cartera])

        fig1 = px.line(to_plot
                        , x="Fecha_reporte"
                        , y="Metric"
                        , color="Vista"
                       )
        fig1["data"][0]["line"]["color"] = "black"

        fig1.layout.yaxis.tickformat = ',.2%'
        

    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')
    fig1.update_layout(
        xaxis_title="Fecha reporte"
        , yaxis_title=kpi_selected
    )


    csv_metricas = convert_df(to_plot
                              .filter(["Vista", "Fecha_reporte", "Metric"])
                              .sort_values(by=["Vista", "Fecha_reporte"], ignore_index=True)
                              )

    col5.download_button(
        label="Descargar CSV",
        data=csv_metricas,
        file_name='Metricas.csv',
        mime='text/csv',
    )
    st.markdown("**Definición métrica:** "+kpi_des)
    zoom = st.checkbox("¿Hacer zoom a la gráfica?")
    if zoom and not flag:
        fig1.update_yaxes(range=[0, 1])

    st.plotly_chart(fig1
                    , use_container_width=True
                    , height = 450
                    , theme="streamlit"
                    )
    del fig1










    #
    # ROLLS
    #
    st.markdown('### Rolls')
    _, _, _, _, _, _, d = st.columns(7)
    csv1 = convert_df(rolls_toplot
                      .filter(list(rolls_toplot)[3:][::-1])
    )
    d.download_button(
        label="Descargar CSV",
        data=csv1,
        file_name='rolls.csv',
        mime='text/csv',
    )
    st.dataframe(rolls_toplot
                 .filter(list(rolls_toplot)[3:][::-1])
                 , use_container_width=False)
    
    rolls_dropdown = list(rolls.Roll.unique())
    rolls_dropdown.sort()
    c1, _, _, _, _ = st.columns(5)
    kpi_selected = c1.selectbox("Selecciona un ROLL:", 
                                ["Todos"] + rolls_dropdown
                               )
    st.write("(Doble click en la leyenda para aislar la curva)")
    
    #kpi_selected = "Todos"
    _query = "Roll == Roll" if kpi_selected == 'Todos' else "Roll == '%s'" % kpi_selected
    
    
    fig2 = px.line(rolls
                   .query(_query + " and Mes not in %s" % str(list(rolls_toplot)[:3]))
                   .assign(Mes = lambda df: df.Mes.apply(lambda x: date.fromisoformat(x)))
                   .sort_values(by=["Roll", "Mes"], ignore_index=True)
                   , x="Mes"
                   , y="Value"
                   , color="Roll"
                  )
    fig2.layout.yaxis.tickformat = ',.1%'
    fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')
    
    
    st.plotly_chart(fig2
                    , use_container_width=True
                    , height = 450
                    , theme="streamlit"
                    )
    
    
        
        
    #
    # Cosechas
    #
    st.markdown('### Cosechas')
    #z1, _, _, _, _ = st.columns(5)
    #dias = z1.selectbox("Selecciona par:", [0, 8 , 30, 60])
    def diff_month(d1, d2):
        if isinstance(d1, str):
            d1 = datetime.fromisoformat(d1)
        if isinstance(d2, str):
            d2 = datetime.fromisoformat(d2)
        return (d1.year - d2.year) * 12 + d1.month - d2.month
        
    def Bucket_Par8(x):
        if x <= 0 :
            return '0. Bucket_Current'
        elif x >= 1 and x < 8 :
            return '1. Bucket_1_7'
        elif x >= 8 and x < 60 :
            return '2. Bucket_8_59'
        elif x >= 60 and x < 90 :
            return '3. Bucket_60_89'
        elif x >= 90 and x < 120 :
            return '4. Bucket_90_119'
        elif x >= 120 :
            return '5. Bucket_120_more'
    
    fechas = ", ".join(["'%s'" % str(d)[:10] for d in pd.date_range("2020-01-31", periods=150, freq="M")])
    _query = " and ".join([f for f in filtro_BQ.split(" and ") if "Fecha_reporte" not in f])
    df_cosechas = (BQ
                   .assign(Dias_de_atraso = lambda df: df.Dias_de_atraso.apply(lambda x: max(x, 0)))
                   #.query("Dias_de_atraso >= %i" % 60)
                   .query("%s and Fecha_reporte in (%s)" 
                          % (_query, fechas)
                          )
                   .assign(Bucket_2 = lambda df: df.Dias_de_atraso.apply(Bucket_Monthly)
                           , Bucket_par8 = lambda df: df.Dias_de_atraso.apply(Bucket_Par8)
                           )
                   .rename(columns={"balance": "Saldo"})
                   .sort_values(by=["ID_Credito", "Fecha_reporte"], ignore_index=True)
                  )
     
    df_cosechas["t"] = df_cosechas.assign(t=range(len(df_cosechas))).groupby(["ID_Credito"]).t.rank()
    df_cosechas["Cosecha"] = df_cosechas.apply(lambda row: "M"+str(diff_month(row["Fecha_reporte"], row["Fecha_apertura"])).zfill(3), axis=1)
    df_cosechas["Mes_apertura"] = df_cosechas["Fecha_apertura"].apply(str).str[:7]
    fecha_reporte_max = df_cosechas.Fecha_reporte.sort_values().iloc[-1]
        
      
    df_cosechas = (df_cosechas
                  .merge(df_cosechas
                         .assign(t=lambda df: df.t+1)
                         [["ID_Credito", "Dias_de_atraso", "Fecha_reporte", "t"]]
                         , on=["ID_Credito", "t"]
                         , suffixes=("", "_ant")
                         , how="left")
                  
                 )
        
    Cosechas = (df_cosechas
                .groupby(["Mes_apertura", "Cosecha"])
                .agg(Saldo = pd.NamedAgg("Saldo", "sum")
                     , Creditos = pd.NamedAgg("ID_Credito", "nunique"))
                .reset_index()
                .filter(['Mes_apertura', 'Cosecha', 'Saldo', 'Creditos'])
                .assign(F = lambda df: df.Mes_apertura.apply(lambda x: int(x.replace("-","")) >= 202108))
                .query("F")
                .drop(columns="F")
                
               )
    
    Cosechas_toshow = (Cosechas
                       .pivot(index="Mes_apertura"
                              , columns="Cosecha"
                              , values="Saldo"
                             )
                       .applymap(lambda x: "${:,.0f}".format(x) if x == x else x)
                       .fillna("")
                       )  
    _, _, _, _, _, _, d = st.columns(7)
    csv2 = convert_df(Cosechas_toshow)
    d.download_button(
        label="Descargar CSV",
        data=csv2,
        file_name='cosechas.csv',
        mime='text/csv',
    )
    st.dataframe(Cosechas_toshow
                 , height=666
                 , use_container_width=True)
    
    ##
    ## Cosechas buckets
    ##
    
    df_agg = (df_cosechas
              .assign(F = lambda df: df.Mes_apertura.apply(lambda x: int(x.replace("-","")) >= 202108))
              .query("F")
              .drop(columns="F")
              .rename(columns={"Cosecha": "index"})
              .pivot_table(index=["Mes_apertura", "Bucket_2"]
                           , columns=["index"]
                           , values="Saldo"
                           , aggfunc="sum")
              .reset_index()
              .fillna(0)
              .rename(columns={"Mes_apertura": "Cosecha"
                               , "Bucket_2": "Bucket"})
              
             )
    
    df_agg = (df_agg
             [["Cosecha"]]
             .drop_duplicates()
             .assign(f=1)
             .merge(df_agg
                    [["Bucket"]]
                    .drop_duplicates()
                    .assign(f=1)
                    , how="left"
                   )
              .assign(f=1)
             .drop(columns="f")
             .merge(df_agg
                    , how="left")
             .fillna(0)
                      .sort_values(by=["Cosecha", "Bucket"], ignore_index=True)
            )
     
    delta = (df_cosechas
             .assign(F = lambda df: df.Mes_apertura.apply(lambda x: int(x.replace("-","")) >= 202108))
             .query("Dias_de_atraso >= 120 and Dias_de_atraso_ant < 120 and F")
             .drop(columns="F")
             .assign(Bucket = "6. WO")
             .groupby(["Cosecha", "Mes_apertura", "Bucket"])
             .agg(Value = pd.NamedAgg("Saldo", "sum"))
             .reset_index()
             .rename(columns={"Mes_apertura": "Cosecha"
                              , "Cosecha": "Mes"
                             })
            )   
    
    df_agg2 = (df_agg
               .melt(id_vars=["Cosecha", "Bucket"]
                     , var_name="Mes"
                     , value_name="Value"
                    )
              )
    df_agg2 = pd.concat([df_agg2
                         , (df_agg2
                            [["Mes"]]
                            .drop_duplicates()
                            .assign(f=1)
                            .merge(df_agg2
                                   [["Cosecha"]]
                                   .drop_duplicates()
                                   .assign(f=1))
                            .drop(columns="f")
                            .merge(delta
                                   , how="left")
                            .fillna({"Bucket": "6. WO"
                                     , "Value": 0})
                           )
                        ])
    df_agg = (df_agg2
              .pivot(index=["Cosecha", "Bucket"]
                     , columns="Mes"
                     , values="Value"
                    )
              .reset_index()
             )
    
    Cosecha_dropdown = list(df_agg.Cosecha.unique())
    Cosecha_dropdown.sort()
    k1, _, _, _, _ = st.columns(5)
    Cosecha_selected = k1.selectbox("Selecciona una cosecha:"
                                    , Cosecha_dropdown
                                    )
    df_agg = (df_agg
              [["Cosecha"]]
              .drop_duplicates()
              .assign(f=1)
              .merge(pd.DataFrame({"Bucket": ["0. Bucket_Current"
                                              , "1. Bucket_1_29"
                                              , "2. Bucket_30_59"
                                              , "3. Bucket_60_89"
                                              , "4. Bucket_90_119"
                                              , "5. Bucket_120_more"
                                              , "6. WO"
                                              ]})
                     .assign(f=1)
                     )
              .drop(columns="f")
              .merge(df_agg, how="left")
              .fillna(0)
             )
    
    
    Cosecha_Bucket = (df_agg[df_agg.Cosecha == Cosecha_selected]
                      .applymap(lambda x: "${:,.0f}".format(x) if not isinstance(x, str) else x)
                      )



    _, _, _, _, _, _, d = st.columns(7)
    csv3 = convert_df(Cosecha_Bucket)
    d.download_button(
        label="Descargar CSV",
        data=csv3,
        file_name='Cosecha_Bucket_%s.csv' % Cosecha_selected,
        mime='text/csv'
    )
    
    st.dataframe(Cosecha_Bucket
                 .assign(Bucket = lambda df: df["Bucket"].apply(lambda x: "6. WO (delta)" if "WO" in x else x))
                 .reset_index(drop=True)
                 , use_container_width=True)
    
    
    WO_Total = (df_agg2
                .assign(Ult_reporte = fecha_reporte_max
                        , Dif = lambda df: (df
                                            .apply(lambda row: diff_month(row["Ult_reporte"], row["Cosecha"]+"-01")
                                                   if row["Cosecha"] != 'Promedio General' else 50
                                                   , 1)
                                           )
                        , Mes_int = lambda df: df.Mes.apply(lambda x: int(x[1:]))
                       )
                .query("Dif >= Mes_int and Bucket.str.contains('WO')")
                .sort_values(by=["Cosecha", "Mes"]
                             , ascending=[True, False]
                             , ignore_index=True
                            )
                #.groupby(["Cosecha"])
               )
    WO_Total["t"] = (WO_Total
                     .assign(t = range(len(WO_Total)))
                     .groupby(["Cosecha"])
                     .agg({"t": "rank"})
                    )
    WO_Total.query("t <= 12", inplace=True)
    
    WO_Total = (WO_Total
                 .groupby(["Cosecha"])
                 .agg({"Value": "sum"
                       , "t": "max"
                      })
                 .reset_index()
                 .assign(Value = lambda df: round(12*df.Value/df.t, 2))
                .drop(columns="t")
                )
    
    ###
    ##  Par 30
    ###
    
    meses = [c for c in df_agg.columns if 'M' in c]
    meses.sort()
    
    pares_total = pd.DataFrame()
    for i, cosecha in enumerate(df_agg.Cosecha.unique()):
        tmp = df_agg.query("Cosecha == '%s'" % cosecha).copy().reset_index(drop=True)
        pares = {"Cosecha": [cosecha, cosecha, cosecha]
                 ,"KPI": ["1.Numerador", "2.Denominador", "Par30"]}
        for m in meses:
            OS_31more = tmp[m].loc[2:4].sum()
            WO_cumulative = tmp[meses[:meses.index(m)+1]].loc[6].sum()
            
            Total = tmp[m].loc[:4].sum()
            
            pares[m] = [OS_31more + WO_cumulative
                        , Total + WO_cumulative
                        , (OS_31more + WO_cumulative)/(Total + WO_cumulative + 0.000001)
                       ]
        pares_total = pd.concat([pares_total, pd.DataFrame(pares)], ignore_index=True)
       
    pares_total = pares_total.melt(id_vars=["Cosecha", "KPI"]
                                   , var_name="Mes"
                                   , value_name='Value'
                                  )
    
    pares_total = (
        pares_total
     .assign(Ult_reporte = fecha_reporte_max
             , Dif = lambda df: (df
                                 .apply(lambda row: diff_month(row["Ult_reporte"], row["Cosecha"]+"-01")
                                         if row["Cosecha"] != 'Promedio General' else 50
                                         , 1)
                                )
             , Mes_int = lambda df: df.Mes.apply(lambda x: int(x[1:]))
            )
     .query("Dif >= Mes_int and KPI == 'Par30'")
     .drop(columns=["Ult_reporte", "Dif", "Mes_int"])
    )
    
    Prom_General = (pares_total
                    .merge(Cosechas
                           .rename(columns={"Mes_apertura": "Cosecha"
                                            , "Cosecha": "Mes"
                                           })
                           [["Mes", "Cosecha", "Saldo"]]
                           , how="left")
                    .merge(Cosechas
                           .rename(columns={"Mes_apertura": "Cosecha"
                                            , "Cosecha": "Mes"
                                           })
                           .groupby("Mes")
                           .agg(SaldoTotal = pd.NamedAgg("Saldo", "sum"))
                           .reset_index()
                           , how="left")
                    .assign(Value = lambda df: df.Value*df.Saldo/df.SaldoTotal
                            , Cosecha = "Promedio General")
                    .groupby(["Cosecha", "KPI", "Mes"])
                    .agg({"Value": "sum"})
                    .reset_index()
                   )
    KPIS_pares = pd.concat([pares_total, Prom_General])
    
    ###
    ##  Par 8
    ###
    df_agg = (df_cosechas
              .assign(F = lambda df: df.Mes_apertura.apply(lambda x: int(x.replace("-","")) >= 202108))
              .query("F")
              .drop(columns="F")
              .rename(columns={"Cosecha": "index"})
              .pivot_table(index=["Mes_apertura", "Bucket_par8"]
                           , columns=["index"]
                           , values="Saldo"
                           , aggfunc="sum")
              .reset_index()
              .fillna(0)
              .rename(columns={"Mes_apertura": "Cosecha"
                               , "Bucket_par8": "Bucket"}) 
             )
    
    df_agg = (df_agg
             [["Cosecha"]]
             .drop_duplicates()
             .assign(f=1)
             .merge(df_agg
                    [["Bucket"]]
                    .drop_duplicates()
                    .assign(f=1)
                    , how="left"
                   )
             .drop(columns="f")
             .merge(df_agg
                    , how="left")
             .fillna(0)
                      .sort_values(by=["Cosecha", "Bucket"], ignore_index=True)
            )
    
    delta = (df_cosechas
             .assign(F = lambda df: df.Mes_apertura.apply(lambda x: int(x.replace("-","")) >= 202108))
             .query("Dias_de_atraso >= 120 and Dias_de_atraso_ant < 120 and F")
             .drop(columns="F")
             .assign(Bucket = "6. WO")
             .groupby(["Cosecha", "Mes_apertura", "Bucket"])
             .agg(Value = pd.NamedAgg("Saldo", "sum"))
             .reset_index()
             .rename(columns={"Mes_apertura": "Cosecha"
                              , "Cosecha": "Mes"
                             })
            )
    
    df_agg2 = (df_agg
               .melt(id_vars=["Cosecha", "Bucket"]
                     , var_name="Mes"
                     , value_name="Value"
                    )
              )
    df_agg2 = pd.concat([df_agg2
                         , (df_agg2
                            [["Mes"]]
                            .drop_duplicates()
                            .assign(f=1)
                            .merge(df_agg2
                                   [["Cosecha"]]
                                   .drop_duplicates()
                                   .assign(f=1))
                            .drop(columns="f")
                            .merge(delta
                                   , how="left")
                            .fillna({"Bucket": "6. WO"
                                     , "Value": 0})
                           )
                        ])
    df_agg = (df_agg2
              .pivot(index=["Cosecha", "Bucket"]
                     , columns="Mes"
                     , values="Value"
                    )
              .reset_index()
             )
    
    pares_total = pd.DataFrame()
    for i, m in enumerate(df_agg.Cosecha.unique()):
        tmp = df_agg.query("Cosecha == '%s'" % m).copy().reset_index(drop=True)
        pares = {"Cosecha": [m, m, m]
                 ,"KPI": ["1.Numerador", "2.Denominador", "Par8"]}
        for m in meses:
            OS_31more = tmp[m].loc[2:4].sum()
            WO_cumulative = tmp[meses[:meses.index(m)+1]].loc[6].sum()
            
            Total = tmp[m].loc[:4].sum()
            
            pares[m] = [OS_31more + WO_cumulative
                        , Total + WO_cumulative
                        , (OS_31more + WO_cumulative)/(Total + WO_cumulative + 0.000001)
                       ]
        pares_total = pd.concat([pares_total, pd.DataFrame(pares)], ignore_index=True)
        
    pares_total = pares_total.melt(id_vars=["Cosecha", "KPI"]
                                   , var_name="Mes"
                                   , value_name='Value'
                                  )
    
    pares_total = (
        pares_total
     .assign(Ult_reporte = fecha_reporte_max
             , Dif = lambda df: (df
                                 .apply(lambda row: diff_month(row["Ult_reporte"], row["Cosecha"]+"-01")
                                         if row["Cosecha"] != 'Promedio General' else 50
                                         , 1)
                                )
             , Mes_int = lambda df: df.Mes.apply(lambda x: int(x[1:]))
            )
     .query("Dif >= Mes_int and KPI.str.contains('Par')")
     .drop(columns=["Ult_reporte", "Dif", "Mes_int"])
    )
    
    Prom_General = (pares_total
                    .merge(Cosechas
                           .rename(columns={"Mes_apertura": "Cosecha"
                                            , "Cosecha": "Mes"
                                           })
                           [["Mes", "Cosecha", "Saldo"]]
                           , how="left")
                    .merge(Cosechas
                           .rename(columns={"Mes_apertura": "Cosecha"
                                            , "Cosecha": "Mes"
                                           })
                           .groupby("Mes")
                           .agg(SaldoTotal = pd.NamedAgg("Saldo", "sum"))
                           .reset_index()
                           , how="left")
                    .assign(Value = lambda df: df.Value*df.Saldo/df.SaldoTotal
                            , Cosecha = "Promedio General")
                    .groupby(["Cosecha", "KPI", "Mes"])
                    .agg({"Value": "sum"})
                    .reset_index()
                   )
    
    KPIS_pares = pd.concat([KPIS_pares, pares_total, Prom_General])
    
    KPIS_pares = pd.concat([KPIS_pares, WO_Total.assign(KPI="WO anual", Mes = 'M012')])
    
    st.markdown("### Par 8")
    

    
    
    
    
    to_plot_par8 = (pd.concat([KPIS_pares
                               .query("Cosecha != 'Promedio General' and KPI == 'Par8'")
                               , KPIS_pares_df.query("Cosecha == 'Promedio General' and KPI == 'Par8'")
                          ])
               
              )

    _, _, _, _, _, _, d = st.columns(7)
    csv4 = convert_df(to_plot_par8.pivot_table(index=["Mes"], columns=["Cosecha"], values="Value").fillna("") )
    d.download_button(
        label="Descargar CSV",
        data=csv4,
        file_name='par8.csv',
        mime='text/csv'
    )
    st.write("Doble click en la leyenda para aislar")

    fig3 = px.line(to_plot_par8
                   , x="Mes"
                   , y="Value"
                   , color="Cosecha"
                  )
    fig3.update_traces(line=dict(width=0.8))
    
    
    
    for i in range(len(fig3['data'])):
        if fig3['data'][i]['legendgroup'] == 'Promedio General':
            fig3['data'][i]['line']['color'] = 'black'
            fig3['data'][i]['line']['width'] = 1.2
        if fig3['data'][i]['legendgroup'] == '2022-05':
            fig3['data'][i]['line']['color'] = 'brown'
    
    
    
    fig3.layout.yaxis.tickformat = ',.1%'
    fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')
    st.plotly_chart(fig3
                    , use_container_width=True
                    , height = 450
                    , theme="streamlit"
                    )
    
    st.markdown("### Par 30")
    

    
    
    
    to_plot_par30 = (pd.concat([KPIS_pares
                                .query("Cosecha != 'Promedio General' and KPI == 'Par30'")
                                , KPIS_pares_df.query("Cosecha == 'Promedio General' and KPI == 'Par30'")
                          ])
               
              )
    _, _, _, _, _, _, d = st.columns(7)
    csv5 = convert_df(to_plot_par30.pivot_table(index=["Mes"], columns=["Cosecha"], values="Value").fillna(""))
    d.download_button(
        label="Descargar CSV",
        data=csv5,
        file_name='par30.csv',
        mime='text/csv'
    )
    st.write("Doble click en la leyenda para aislar")
    
    fig3 = px.line(to_plot_par30
                   , x="Mes"
                   , y="Value"
                   , color="Cosecha"
                  )
    fig3.update_traces(line=dict(width=0.8))
    
    
    
    for i in range(len(fig3['data'])):
        if fig3['data'][i]['legendgroup'] == 'Promedio General':
            fig3['data'][i]['line']['color'] = 'black'
            fig3['data'][i]['line']['width'] = 1.2
        if fig3['data'][i]['legendgroup'] == '2022-05':
            fig3['data'][i]['line']['color'] = 'brown'
    
    
    
    fig3.layout.yaxis.tickformat = ',.1%'
    fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')
    
    #st.dataframe(to_plot_par30)
    
    st.plotly_chart(fig3
                    , use_container_width=True
                    , height = 450
                    , theme="streamlit"
                    )
    
    st.markdown("### Zoom Par 30 Mob 3")
    
    Par30Mob3 = (to_plot_par30
                 .query("Mes == 'M003'")
                 .sort_values(by=["Value"]
                              , ascending=[False]
                              , ignore_index=True
                              )
                 .assign(Cosecha = lambda df: df.Cosecha.apply(lambda x: "Promedio" if "Promedio" in x else str(x))
                         , color = lambda df: df.Cosecha.apply(lambda x: "red" if "Promedio" in x else 'blue')

                         )
                )
    Par30Mob3['category'] = [str(i) for i in Par30Mob3.index]
    
      
    fig4 = px.bar(Par30Mob3
                 , y='Value'
                 , x='Cosecha'
                 , color="category"
                 , color_discrete_sequence=list(Par30Mob3["color"].values)
                 , text_auto=',.1%'
                )
    fig4.layout.yaxis.tickformat = ',.1%'
    fig4.layout.xaxis.type = 'category'
    fig4.update_traces(textfont_size=12
                      , textangle=0
                      , textposition="inside"
                      , cliponaxis=False
                      )
    fig4.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')
    st.plotly_chart(fig4
                    , use_container_width=True
                    , height = 450
                    , theme="streamlit"
                    )
    

    
    # Row C
    


st.sidebar.write("")
#st.sidebar.write("")
#if st.sidebar.button('Descargar reporte (Excel)'):
#    def find_downloads():
#        if os.name == 'nt':
#            import winreg
#            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
#            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
#            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
#                location = winreg.QueryValueEx(key, downloads_guid)[0]
#            return location
#        else:
#            return os.path.join(os.path.expanduser('~'), 'downloads')
#    st.sidebar.write('Reporte descargado en tu carpeta de descargas:')
#    st.sidebar.write(str(find_downloads()))
#else:
#    st.sidebar.write("")
#    st.sidebar.write("")
