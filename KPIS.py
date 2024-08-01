# Erick Santillan

import json
import streamlit as st
import os
import pandas as pd
# import pandas_gbq
import plotly.express as px
import requests


from datetime import datetime, timedelta, date
from plotly import graph_objs as go
from PIL import Image
from st_pages import show_pages_from_config, add_page_title, show_pages, Page



# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar


url = "https://v.fastcdn.co/u/c2e5d077/58473217-0-Logo.png"
img = Image.open(requests.get(url, stream=True).raw)
show_pages_from_config()




st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title="KPIS de riesgo", page_icon=img)
st.title("KPIS de riesgo")
# Optional -- adds the title and icon to the current page

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("streamlit_app_web.py", "KPIS de riesgo", "")
    ]
)



def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def diff_month(d1, d2):
    # d1 sea la fecha mayor y d2 la fecha menor
    if isinstance(d1, str):
        d1 = datetime.fromisoformat(d1)
    if isinstance(d2, str):
        d2 = datetime.fromisoformat(d2)
    return (d1.year - d2.year) * 12 + d1.month - d2.month

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

def format_column(df, column):
    flag = False
    if column == "Edad": 
        df["Edad_formato"] = (df["Edad"]
                            .apply(lambda x: "De %i a %i" % (int(x//5)*5, int(x//5)*5+4))
                            .replace({"De 60 a 64": "Mayor de 60"
                                      , "De 65 a 69": "Mayor de 60"
                                      , "De 70 a 74": "Mayor de 60"
                                      , "De 75 a 79": "Mayor de 60"
                                      , "De 80 a 84": "Mayor de 60"
                                      , "De 20 a 24": "De 20 a 29"
                                      , "De 25 a 29": "De 20 a 29"
                                      }))
        flag = True
    elif column == "genero_estimado":
        factor_dict = {"Todos": "Todos", "Hombre": "H", "Mujer": "M", "Vacio": "?"}
        factor_dict = {value:key for (key, value) in factor_dict.items()}
        df["genero_estimado_formato"] = df["genero_estimado"].apply(lambda x: factor_dict[x])
        flag = True
    elif column == "term_type":
        factor_dict = {"Todos": "Todos", "W": "Semanal", "B": "Catorcenal", "M": "Mensual"}
        df["term_type_formato"] = df["term_type"].apply(lambda x: factor_dict[x])
        flag = True
    elif column == "Municipio":
        df = df.merge(st.session_state["cat_municipios"]
                      .assign(Municipio_formato = (st.session_state["cat_municipios"]["Estado"].replace({'E': 'Edo Mex', 'C': 'CDMX', 'H': 'Hgo', 'P': 'Pue', 'J': 'Jal', 'T': 'Tlaxcala'})
                                                   + ", " + st.session_state["cat_municipios"]["Municipio"])
                            )
                      .filter(["CP", "Municipio_formato"])
                      .drop_duplicates()
                      , how="left"
                      , on="CP"
                     )
        flag = True
    elif column == "Estado":
        df = df.merge(st.session_state["cat_municipios"]
                      
                      .filter(["CP", "Estado"])
                      .drop_duplicates()
                      .rename(columns={"Estado": "Estado_formato"})
                      , how="left"
                      , on="CP"
                    )
        df["Estado_formato"] = df["Estado_formato"].replace({'E': 'Edo Mex', 'C': 'CDMX', 'H': 'Hgo', 'P': 'Pue', 'J': 'Jal', 'T': 'Tlaxcala'})
        flag = True
    elif column == "industry":
        df = df.merge(st.session_state["cat_industry"]
                      .filter(["industry", "industry_cve"])
                      .drop_duplicates()
                      .rename(columns={"industry": "industry_formato"})
                      , how="left"
                      , on="industry_cve"
                     )
        flag = True
    elif column == "Analista":
        df = df.merge(st.session_state["cat_advisors"]
                        .filter(["Analista", "Cartera_YoFio"])
                        .drop_duplicates()
                        .rename(columns={"Analista": "Analista_formato"})
                        , how="left"
                        , on="Cartera_YoFio"
                         )
        flag = True
    elif column == 'ZONA':
        df = df.merge(st.session_state["cat_advisors"]
                        .filter(["ZONA", "Cartera_YoFio"])
                        .drop_duplicates()
                        .rename(columns={"ZONA": "ZONA_formato"})
                        , how="left"
                        , on="Cartera_YoFio"
                         )
        flag = True
    elif column == 'n_ampliaciones':
        df = df.assign(n_ampliaciones_formato = df["n_ampliaciones"].apply(lambda x: "%i" % x if x < 4 else "4+"))
        flag = True


    return flag, df


def get_date(i):
    return str(datetime.fromisoformat("2023-01-01")+timedelta(days=7*i))[:10]

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

def roi_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    if vista == "Mes":
        _to_group.pop(0)
    return (dataframe
            .assign(roi = dataframe["ingreso_cumulative"]-dataframe["total_amount_disbursed_cumulative"])
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("roi", "sum"))
            .reset_index()
            .filter(_to_group + ["Metric"])
           )

def roi_ratio_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    if vista == "Mes":
        _to_group.pop(0)
    return (dataframe
            .groupby(_to_group)
            .agg(ingreso = pd.NamedAgg("ingreso_cumulative", "sum")
                 , desembolso = pd.NamedAgg("total_amount_disbursed_cumulative", "sum")
                )
            .assign(Metric = lambda df: df["ingreso"] / df["desembolso"])
            .reset_index()
            .filter(_to_group + ["Metric"])
           )

def roi_interes_ratio_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    if vista == "Mes":
        _to_group.pop(0)

    return (dataframe
            .groupby(_to_group)
            .agg(ingreso = pd.NamedAgg("interes_cumulative", "sum")
                 , desembolso = pd.NamedAgg("total_amount_disbursed_cumulative", "sum")
                )
            .assign(Metric = lambda df: df["ingreso"] / df["desembolso"])
            .reset_index()
            .filter(_to_group + ["Metric"])
           )


def Default_rate_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    if vista == "Mes":
        _to_group.pop(0)
    return (dataframe
            .assign(OS120 = (dataframe["Dias_de_atraso"]>=120).astype(int) * dataframe["balance"]
                    , balance = dataframe["balance"]
                    , antiguedad = (pd.to_datetime(dataframe["Fecha_reporte"]) - pd.to_datetime(dataframe["Fecha_apertura"])).dt.days/30
                    , N_OS120 = (dataframe["Dias_de_atraso"]>=120).astype(int)
                    , N_balance = (dataframe["Dias_de_atraso"]<120).astype(int)
                   )
            .groupby(_to_group)
            .agg({"OS120": "sum", "balance": "sum", "N_OS120": "sum", "N_balance": "sum", "antiguedad": "mean"})
            .reset_index()
            # .assign(Metric = lambda df: 12 * (df["OS120"] / df["balance"] ) / df["antiguedad"])
            .assign(Metric = lambda _df: _df["OS120"] / _df["balance"]  )
            .filter(_to_group + ["Metric"])

           )

def lim_credito_avg_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    return (dataframe
            .query("Status_credito != 'I'")
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("Monto_credito", "mean"))
            .reset_index()
            .filter(_to_group + ["Metric"])
           )

def current_pct_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            
            .assign(Current = dataframe["Bucket"].str.contains('Current') * dataframe["balance"])
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group)
            .agg({"Current": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["Current"] / (df["balance"] + (df["balance"] == 0).astype(int)))
            .filter(_to_group + ["Metric"])

           )


def current_sin_ip_pct_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            
            .assign(Current = dataframe["Bucket"].str.contains('Current') * dataframe["balance_sin_ip"])
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group)
            .agg({"Current": "sum", "balance_sin_ip": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["Current"] / (df["balance_sin_ip"] + (df["balance_sin_ip"] == 0).astype(int)))
            .filter(_to_group + ["Metric"])

           )

def total_amount_disbursed_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    return (dataframe
            .groupby(_to_group, as_index=False)
            .agg(Metric = pd.NamedAgg("total_amount_disbursed_cumulative", "sum"))
            .filter(_to_group + ["Metric"])
            )

def os_8_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    if vista == "Mes":
        _to_group.pop(0)
    return (dataframe
            .assign(OS8 = (dataframe["Dias_de_atraso"]>=8).astype(int) * dataframe["balance"])
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group)
            .agg({"OS8": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["OS8"] / df["balance"])
            .filter(_to_group + ["Metric"])

           )

def os_30_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    if vista == "Mes":
        _to_group.pop(0)

    return (dataframe
            .assign(OS30 = (dataframe["Dias_de_atraso"]>=30).astype(int) * dataframe["balance"])
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group)
            .agg({"OS30": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["OS30"] / df["balance"])
            .filter(_to_group + ["Metric"])
           )

def os_30_task_con_WO(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    if vista == "Mes":
        _to_group.pop(0)

    return (dataframe
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
            .assign(OS60 = (dataframe["Dias_de_atraso"]>=60).astype(int) * dataframe["balance"])
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group)
            .agg({"OS60": "sum", "balance": "sum"})
            .reset_index()
            .assign(Metric = lambda df: df["OS60"] / df["balance"])
            .filter(_to_group + ["Metric"])

           )

def os_90_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .assign(OS60 = (dataframe["Dias_de_atraso"]>=90).astype(int) * dataframe["balance"])
            .query("Bucket.str.contains('120') == False")
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
            .query("Dias_de_atraso < 120")
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

def credit_limit(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("Monto_credito", "sum"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def metrica_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]
    


    _df = (dataframe
            .groupby(_to_group, as_index=False)
            .agg(Metric=pd.NamedAgg("Monto_credito", "sum"))
            .filter(_to_group + ["Metric"])
           )

    return _df 

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
            .query("Status_credito=='L'") # LATE
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("balance", "sum"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def imora_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    _x =  (dataframe
            .assign(balance_limpio = dataframe["balance"] * (dataframe["Dias_de_atraso"]<120).astype(int)
                    , delta = dataframe["balance"] * ((dataframe["Dias_de_atraso"]>=120) & (dataframe["Dias_de_atraso_ant"]<120)).astype(int)
                   )
            .groupby(_to_group, as_index=False)
            .agg(balance_limpio = pd.NamedAgg("balance_limpio", "sum")
                 , delta = pd.NamedAgg("delta", "sum")
                 )
            # Sumar últimos 12 deltas por cada Fecha_reporte
            .sort_values(by=_to_group[::-1], ignore_index=True)
            .assign(dummies = 1)
            )
    _vista = vista if vista != "" else "dummies"
            
    return (_x
            .assign(delta_12m = lambda df: df.groupby(_vista)["delta"].rolling(window=12, min_periods=1).sum().reset_index(drop=True))
            .assign(Metric = lambda df: df["delta_12m"] / (df["balance_limpio"] + df["delta_12m"] + (df["balance_limpio"] + df["delta_12m"] == 0).astype(int)))
            .filter(_to_group + ["Metric"])
           )

def delta_pct_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    _x =  (dataframe
            .assign(delta = dataframe["balance"] * ((dataframe["Dias_de_atraso"]>=120) & (dataframe["Dias_de_atraso_ant"]<120)).astype(int)
                    , balance_limpio = dataframe["balance"] * (dataframe["Dias_de_atraso"]<120).astype(int)
                   )
            .groupby(_to_group, as_index=False)
            .agg(delta = pd.NamedAgg("delta", "sum")
                 , balance = pd.NamedAgg("balance_limpio", "sum")
                 )
            .sort_values(by=_to_group[::-1], ignore_index=True)
            .assign(dummies = 1)
            )
    _vista = vista if vista != "" else "dummies"
            
    return (_x
            .assign(delta_12m = lambda df: df.groupby(_vista)["delta"].rolling(window=12, min_periods=1).sum().reset_index(drop=True))
            .assign(Metric = lambda df: 12* df["delta"] / (df["balance"] + df["delta_12m"] + (df["balance"] + df["delta_12m"] == 0).astype(int)))
            # .assign(Metric = lambda df: df["delta_12m"] )
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
            .query("Status_credito.isin(['L', 'C'])") # LATE & CURRENT
            .groupby(_to_group)
            .agg(Metric = pd.NamedAgg("ID_Credito", "nunique"))
            .reset_index()
            .filter(_to_group + ["Metric"])

           )

def Mora_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .query("Status_credito.isin(['L'])") # LATE
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
    t = pd.concat([saldos
                    .query("Bucket.str.contains('120') == False")
                    , _df
                       .query("Dias_de_atraso >= 120 and Dias_de_atraso_ant < 120")
                       .assign(Bucket = "%s. delta" % str(N+1).zfill(2 - int(N+1 < 10)))
                       .groupby(["Bucket", "Fecha_reporte", vista])
                       .agg(balance = pd.NamedAgg("balance", "sum"))
                       .reset_index()])

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

def perdida_hasta_120_task(dataframe, vista):
    _df = dataframe.copy()
    if vista == "":
        vista = "P"
        _df[vista] = "P"
    else:
        pass

    No_fechas = list(_df["Fecha_reporte"].unique())
    No_fechas.sort()
    No_fechas = No_fechas[:{"Mensual": 3, "Semanal": 12, "Catorcenal": 6}[cortes]]

    saldos = (_df
              .groupby(["Bucket", "Fecha_reporte", vista])
              .agg({"balance": "sum"})
              .reset_index()
             )
    _df = (_df
            .query("Dias_de_atraso >= 120 and Dias_de_atraso_ant < 120")
            .assign(Bucket = "%s. delta" % str(N+1).zfill(2 - int(N+1 < 10)))
            .groupby(["Bucket", "Fecha_reporte", vista])
            .agg(balance = pd.NamedAgg("balance", "sum"))
            .reset_index()
            )
    t = pd.concat([saldos.query("Bucket.str.contains('120') == False"), _df])
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
                .query("Bucket.str.contains('120') == False")
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



def roll_0_1_task(dataframe, vista):
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

    
    t = (t
         .query("N_Bucket == 0")
         .rename(columns={"Roll": "Metric"})
         .filter(["Fecha_reporte", vista, "Metric"])
        )
    return t.filter(["Fecha_reporte", vista, "Metric"])
            
def os_60_monto_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .assign(Metric = (dataframe["Dias_de_atraso"]>=60).astype(int) * dataframe["balance"])
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group, as_index=False)
            .agg({"Metric": "sum"})
            .filter(_to_group + ["Metric"])
           )

def os_60_cuentas_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    return (dataframe
            .assign(Metric = (dataframe["Dias_de_atraso"]>=60).astype(int))
            .query("Bucket.str.contains('120') == False")
            .groupby(_to_group, as_index=False)
            .agg({"Metric": "sum"})
            .filter(_to_group + ["Metric"])
           )

def tiempo_hasta_primera_ampliacion_task(dataframe, vista):
    _to_group = ["Fecha_reporte", vista] if vista != "" else ["Fecha_reporte"]

    # Calcular la diferencia entre la fecha de apertura y la fecha de la primera ampliación
    x = (st.session_state["BQ"]
         .query("n_ampliaciones == 1")
         .groupby(["ID_Credito"], as_index=False)
         .agg(Fecha_ampliacion = pd.NamedAgg("Fecha_reporte", "min"))
        )

    _df = (dataframe
            .merge(x, how="inner")
            .assign(Fecha_ampliacion = lambda _df: _df.apply(lambda row: row["Fecha_ampliacion"] if row["Fecha_ampliacion"] <= row["Fecha_reporte"] else pd.NaT, axis=1))
            .query("Fecha_ampliacion.notna()")
            .assign(Dias_hasta_primera_ampliacion = lambda _df: (pd.to_datetime(_df["Fecha_ampliacion"]) - pd.to_datetime(_df["Fecha_apertura"])).dt.days)
            .groupby(_to_group, as_index=False)
            .agg(Metric = pd.NamedAgg("Dias_hasta_primera_ampliacion", "mean"))
            .filter(_to_group + ["Metric"])
           )
    return _df


###########################################
# Data
###########################################

if "BQ" not in st.session_state:
    
    ###########################################
    #  Catalogos
    ###########################################
    st.session_state["cat_advisors"] = pd.read_csv("Data/cat_advisors.csv")
    st.session_state["cat_advisors"].loc[st.session_state["cat_advisors"]["Cartera_YoFio"] == 'C044', ["Analista"]] = "Adriana Alcantar"
    st.session_state["cat_advisors"].loc[st.session_state["cat_advisors"]["ZONA"] == 'Iztacalco', ["ZONA"]] = "Nezahualcoyotl"

    st.session_state["cat_municipios"] = pd.read_csv("Data/cat_municipios.csv", dtype={"CP": str})
    st.session_state["cat_municipios"]["CP"] = st.session_state["cat_municipios"]["CP"].str.zfill(5)
    municipios_list = (st.session_state["cat_municipios"]["Estado"].replace({'E': 'Edo Mex', 'C': 'CDMX', 'H': 'Hgo', 'P': 'Pue', 'J': 'Jal', 'T': 'Tlaxcala'})
                       + ", " + st.session_state["cat_municipios"]["Municipio"]
                      ).fillna('?').unique().tolist()
    municipios_list.sort()
    st.session_state["municipios_list"] = municipios_list

    st.session_state["cat_industry"] = pd.read_csv("Data/cat_industry.csv")
    ###########################################



    ###########################################
    #  BQ
    ###########################################
    fines_de_mes = ", ".join(["'%s'" % str(d)[:10] for d in pd.date_range("2021-03-31", periods=50, freq="M")])
    st.session_state["BQ"] = (pd.concat([pd.read_csv("Data/"+f) for f in os.listdir("Data/") if "BQ_reduced" in f and "csv" in f])
                              .query("(Fecha_reporte in (%s)) or (Fecha_reporte >= '2023-01-01')" % fines_de_mes)
                              .assign(CP = lambda df: df["CP"].fillna(0).astype(int).astype(str).str.zfill(5))
                              .fillna({"Dias_de_atraso": 0})
                              .drop_duplicates()
                             )


    for c in ["Monto_credito", "Dias_de_atraso", "saldo", "balance"]:
        st.session_state["BQ"][c] = st.session_state["BQ"][c].apply(lambda x: float(x) if x!="" else 0)

    st.session_state["BQ"]["Fecha_apertura"] = st.session_state["BQ"]["Fecha_apertura"].str[:7]
    st.session_state["BQ"]["Semestre_cohort"] = st.session_state["BQ"]["Fecha_apertura"].str[:4] + "-" + st.session_state["BQ"]["Fecha_apertura"].str[5:7].apply(lambda x: "01" if int(x) <= 6 else "02")
    st.session_state["BQ"]["Rango"] = st.session_state["BQ"]["Monto_credito"].apply(rango_lim_credito)
    # st.session_state["BQ"]["Status_credito"] = st.session_state["BQ"]["Status_credito"]#.replace({'I': 'INACTIVE', 'C': 'CURRENT', 'A': 'APPROVED', 'L': 'LATE'})
    st.session_state["BQ"]["balance_sin_ip"] = st.session_state["BQ"]["balance"].values
    st.session_state["BQ"]["balance"] = st.session_state["BQ"][["balance", "saldo"]].fillna(0).sum(axis=1)
    st.session_state["BQ"]["Edad"] = (pd.to_datetime(st.session_state["BQ"]["Fecha_reporte"]) - pd.to_datetime(st.session_state["BQ"]["birth_date"])).dt.days / 365.25
    st.session_state["BQ"] = st.session_state["BQ"].drop(columns=["birth_date"])
    st.session_state["BQ"]["Edad"] = st.session_state["BQ"]["Edad"].fillna(st.session_state["BQ"]["Edad"].mean())
    st.session_state["BQ"]["allow_disbursements"] = st.session_state["BQ"]["allow_disbursements"].fillna(0) # 0: Not allowed, 1: Allowed

temp = st.session_state["BQ"].copy()
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


##### Filter term_type on temp
term_type = st.sidebar.multiselect('Selecciona tipo de corte de cartera'
                                 , ('Todos', 'Catorcenal', 'Mensual', 'Semanal')
                                 , default='Todos'
                                 ) 
if "Todos" not in term_type:
    term_type_dict = {'Catorcenal': "B", 'Mensual': "M", 'Semanal': "W"}
    term_type = [term_type_dict[t] for t in term_type]
    temp = temp[temp["term_type"].isin(term_type)]


zona_list = list(st.session_state["cat_advisors"].ZONA.drop_duplicates().values)
zona_list.sort()
zona = st.sidebar.multiselect('Selecciona la zona del analista'
                            , ['Todas'] + zona_list
                            , default='Todas'
                            )
if "Todas" not in zona:
    temp = temp[temp["Cartera_YoFio"].isin(st.session_state["cat_advisors"].loc[st.session_state["cat_advisors"]["ZONA"].isin(zona), "Cartera_YoFio"].values)]



Analista_list = list(st.session_state["cat_advisors"].Analista.dropna().drop_duplicates().values)
Analista_list.sort()
analista = st.sidebar.multiselect('Selecciona el analista'
                                  , ['Todos'] + Analista_list
                                  , default='Todos'
                                 )
if "Todos" not in analista:
    temp = temp[temp["Cartera_YoFio"].isin(st.session_state["cat_advisors"].loc[st.session_state["cat_advisors"]["Analista"].isin(analista), "Cartera_YoFio"].values)]



ampl = st.sidebar.multiselect('Selecciona el número de ampliación'
                                 , ["Todas", 0, 1, 2, 3, "4+"]
                                 , default='Todas'
                                 )

if "Todas" in ampl:
    pass
elif  "4+" not in ampl:
    temp = temp.query("n_ampliaciones.isin(@ampl)")
else:
    temp = temp.query("n_ampliaciones.isin(@ampl) or n_ampliaciones >= 4")

##### Filter genero on temp
genero = st.sidebar.multiselect('Selecciona el género del tiendero'
                                 , ["Todos", "Hombre", "Mujer", "Vacio"]
                                 , default='Todos'
                                 )
genero_dict = {"Todos": "Todos", "Hombre": "H", "Mujer": "M", "Vacio": "?"}
genero = [genero_dict[g] for g in genero]
if "Todos" not in genero:
    temp = temp[temp["genero_estimado"].isin(genero)]

##### Filter cohort on temp
cohort = st.sidebar.multiselect('Selecciona el cohort'
                                , ['Todos'] + list(temp.Fecha_apertura.unique())
                                , default='Todos'
                               )
cohort = [str(c) for c in cohort]
if "Todos" not in cohort:
    temp = temp[temp["Fecha_apertura"].isin(cohort)]
    
##### Filter edad on temp
Edades_list = ["De 20 a 29", "De 30 a 34", "De 35 a 39", "De 40 a 44", "De 45 a 49", "De 50 a 54", "De 55 a 59", "Mayor de 60"]
Edades_list.sort()
edad = st.sidebar.multiselect('Selecciona la edad del tiendero'
                              , ['Todos'] + Edades_list
                              , default='Todos'
                             )
if "Todos" not in edad:
    temp = temp[temp["Edad"]
            .apply(lambda x: "De %i a %i" % (int(x//5)*5, int(x//5)*5+4))
            .replace({"De 60 a 64": "Mayor de 60"
                      , "De 65 a 69": "Mayor de 60"
                      , "De 70 a 74": "Mayor de 60"
                      , "De 75 a 79": "Mayor de 60"
                      , "De 80 a 84": "Mayor de 60"
                      , "De 20 a 24": "De 20 a 29"
                      , "De 25 a 29": "De 20 a 29"
                     })
            .isin(edad)
            ]

estados_list = ["CDMX", "Edo Mex", "Hidalgo", "Jalisco", "Puebla", "Tlaxcala"]
estados_list.sort()
estado = st.sidebar.multiselect('Selecciona el estado de la tienda'
                             , ['Todos'] + estados_list
                             , default='Todos'
                            )
if "Todos" not in estado:
    estado = [e[0] for e in estado]
    temp = (temp
            .merge(st.session_state["cat_municipios"]
                   [st.session_state["cat_municipios"]["Estado"].isin(estado)]
                   .filter(["CP"]))
            )

municipio = st.sidebar.multiselect('Selecciona el municipio de la tienda'
                                 , ['Todos'] + st.session_state["municipios_list"]
                                 , default='Todos'
                                 )
if "Todos" not in municipio:
    temp = temp[temp["CP"].isin(st.session_state["cat_municipios"]
                                [st.session_state["cat_municipios"]["Municipio"].isin(municipio)]
                                ["CP"]
                                .values
                                )
               ]



rangos_list = list(st.session_state["BQ"].Rango.unique())
rangos_list.sort()
rangos = st.sidebar.multiselect('Selecciona el rango del límite de credito'
                                 , ['Todos'] + rangos_list
                                 , default='Todos'
                                 )

industry_list = list(st.session_state["cat_industry"].industry.unique())
industry_list.sort()
industry = st.sidebar.multiselect('Selecciona el giro del negocio'
                                 , ['Todos'] + industry_list
                                 , default='Todos'
                                 )
if "Todos" not in industry:
    temp = temp[temp["industry_cve"].isin(st.session_state["cat_industry"]
                                          [st.session_state["cat_industry"]["industry"].isin(industry)]
                                          ["industry_cve"]
                                          .values
                                          )
                ]

dsoto = st.sidebar.multiselect('¿Evaluación virtual? (dsoto)'
                               , ['Si', 'No']
                               , default=['Si', 'No']
                               )




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


f2 = filtro_dict["f2"]

if 'Todos' in rangos:
    f7 = ""
else:
    f7 = " and Rango.isin(%s)" % str(rangos)



if len(dsoto) == 1:
    f12 = " and Creado_dsoto == %i" % int(dsoto[0] == 'Si')
else:
    f12 = ""



N = filtro_dict["top_rolls"]   
 
filtro_BQ = "Fecha_reporte == Fecha_reporte %s %s " % (f7, f12)
    

YoFio = (st.session_state["BQ"]
         .query("Fecha_reporte in (%s)" % f2)
         .assign(Bucket = lambda df: df.Dias_de_atraso.apply(filtro_dict["Bucket"]))
         .sort_values(by=["ID_Credito", "Fecha_reporte"]
                         , ignore_index=True)
        )
YoFio["Mes"] = YoFio.apply(lambda x: "M" + str(diff_month(x['Fecha_reporte'], x['Fecha_apertura']+"-01")).zfill(3), axis=1)

temp = temp.query(filtro_BQ)
df_cosechas = temp.copy()
temp = (temp
        .query("Fecha_reporte in (%s)" % f2)
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
            .drop(columns=["Fecha_reporte_ant"])
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
            .drop(columns=["Fecha_reporte_ant"])
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
               .query("(not Bucket.str.contains('delta')) and (not Bucket.str.contains('120'))", engine="python")
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

    # try:
    #     from google.oauth2 import service_account
    #     # with open(os.path.join(os.getcwd(), ".streamlit", "gcloud_credentials.json"), "r") as f:
    #     #     credentials = json.load(f)

    #     # credentials = service_account.Credentials.from_service_account_info(credentials)
    #     # pandas_gbq.context.credentials = credentials
    #     # _query = """
    #     # SELECT      COUNT(*) AS N
    #     # FROM        `pivotal-spark-262418.airflow_temp.sales_advisor`
    #     # """ 
    #     # b = (pandas_gbq.read_gbq(_query, project_id="pivotal-spark-262418"))
    #     # _n = b.N.values[0]

    #     # st.write("### Número de cuentas en cartera")
    #     # st.write("#### %i" % _n)
    # except Exception as e:
    #     st.write(e)



    
    st.markdown("### Tamaño cartera (fotografía al %s)" % _max)

    _b1, _b2, _b3 = st.columns(3)
    _b4, _b5 = st.columns(2)
    _b7, _, _, _, _b6 = st.columns(5)

    kpi_sel_0 = _b1.selectbox("Selecciona la métrica", 
                              ["Número de cuentas"
                              , "Cuentas (sin castigo)"
                              , "Cuentas (castigadas)"
                              , "Cuentas activas"
                              , "Cuentas inactivas"
                              , "Cuentas bloqueadas"
                              , "Cuentas bloqueadas 2"
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
                                , "Por cohort"
                                , "Por semestre de cohort"
                                , "Por municipio"
                                , "Por género del tiendero"
                                , "Por giro del negocio"
                                ])
    
    _kpi = {"Número de cuentas": {"y": "account_id", "query": ""}
            , "Cuentas (sin castigo)": {"y": "account_id", "query": "and Dias_de_atraso < 120"}
            , "Cuentas (castigadas)": {"y": "account_id", "query": "and Dias_de_atraso >= 120"}
            , "Cuentas activas": {"y": "account_id", "query": "and Status_credito != 'I' and Dias_de_atraso < 120"}
            , "Cuentas inactivas": {"y": "account_id", "query": "and (Status_credito == 'I' or Dias_de_atraso >= 120)"}
            , "Cuentas bloqueadas 2": {"y": "account_id", "query": "and allow_disbursements == 0 and Status_credito == 'I' and Dias_de_atraso < 120"}
            , "Cuentas bloqueadas": {"y": "account_id", "query": "and allow_disbursements == 0 and Status_credito == 'I' and Dias_de_atraso < 120"}
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
              , "Por cohort": "Fecha_apertura"
              , "Por municipio": "Municipio"
              , "Por semestre de cohort": "Semestre"
              , "Por género del tiendero": "genero_estimado"
              , "Por giro del negocio": "industry"
             }[factor_sel_0]

    comp_sel_0 = _b3.selectbox("Selecciona la comparación", 
                                ["Valores absolutos"
                                , "Valores porcentuales"
                                ])
    
    status_list = ["CURRENT", "APPROVED", "LATE", "INACTIVE"] 
    status_list.sort()
    status_selected = _b4.multiselect("Selecciona el status de la cuenta"
                                      , status_list
                                      , default=status_list
                                    )
    status_selected = [s[0] for s in status_selected]
    flag_sort = _b7.checkbox("Ordenar alfabéticamente", value=False)



    _start, _end = st.select_slider(
        "Selecciona el rango de días de atraso",
        options=list(range(0,122)),
        value=(0, 121)
    )

    formateada, temp = format_column(temp, factor)
    formateada, YoFio = format_column(YoFio, factor)
    factor = factor + "_formato" * int(formateada)

    if _end == 121:
        _end = 10000

    _to_plot = (temp
                .query("Fecha_reporte == '%s'" % _max)
                .query("Dias_de_atraso >= %i and Dias_de_atraso <= %i" % (_start, _end))
                .query("Status_credito.isin(@status_selected)")
                .assign(account_id = 1)
                .query("Fecha_reporte == '%s' %s" % (_max, _kpi["query"]))
                .groupby([factor])
                .agg({"account_id": "sum"
                        , "balance": "sum"})
                .reset_index()
               )
    _to_plot0 = (YoFio
                 .query("Dias_de_atraso >= %i and Dias_de_atraso <= %i" % (_start, _end))
                 .query("Status_credito.isin(@status_selected)")
                 .query("Fecha_reporte == '%s'" % _max)
                 .assign(account_id = 1)
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




    _csv = convert_df(_to_plot)

    _b6.download_button(
        label="Descargar CSV",
        data=_csv,
        file_name='cortes.csv',
        mime='text/csv',
    )


    st.plotly_chart(fig0
                    , use_container_width=True
                    , height = 450
                    , theme="streamlit"
                    )


    st.markdown('### Cortes')
    st.markdown("Saldo de compra de central de abastos o a distribuidor (aún no desembolsado)")

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
    
    _d1, _d2, _d3 = st.columns((4,7,2))
    
    _by = _d1.selectbox("Selecciona la métrica:", ["Por saldo", "Por número de cuentas"])
    agg_by = pd.NamedAgg("balance", "sum") if _by == "Por saldo" else pd.NamedAgg("ID_Credito", "nunique")
    temp_agg_to_show = pd.concat([
        (temp
          .groupby(["Bucket", "Fecha_reporte"])
          .agg(Value = agg_by)
          .reset_index()
          .pivot(index=["Bucket"]
                 , columns="Fecha_reporte"
                 , values="Value"
                 )
          )
        , (temp
           .query("Dias_de_atraso >= 120 and Dias_de_atraso_ant < 120")
           .assign(Bucket = "%s. delta" % str(N+2).zfill(2 - int(N+2 < 10)))
           .groupby(["Bucket", "Fecha_reporte"])
           .agg(Value = agg_by)
           .reset_index()
           .pivot(index="Bucket"
                  , columns="Fecha_reporte"
                  , values="Value"
                  )
           )
        ]).fillna(0)
        
    
    
    cols = list(temp_agg_to_show.columns)[::-1]
    
    temp_agg_to_show = (pd.DataFrame({"Bucket": filtro_dict["buckets"]})
                        .merge(temp_agg_to_show
                                .reset_index()
                                , how="left")
                            .set_index("Bucket")
                            .fillna(0)
                            .filter(cols)
                        )
    
    csv0 = convert_df(temp_agg.reset_index())

    _d3.download_button(
        label="Descargar CSV",
        data=csv0,
        file_name='cortes.csv',
        mime='text/csv',
    )

    
    
    st.dataframe(temp_agg_to_show
                 .applymap(lambda x: "${:,.0f}".format(x) if _by == "Por saldo" else "{:,.0f}".format(x))
                 , use_container_width=True)
    _renamed = "Saldo menor a 120 días" if _by == "Por saldo" else "Cuentas con atraso <120 días"
    st.dataframe(temp_agg_to_show
                 .iloc[:N+1]
                 .sum()
                 .apply(lambda x: "${:,.0f}".format(x) if _by == "Por saldo" else "{:,.0f}".format(x))
                 .to_frame()
                 .transpose()
                 .assign(i="Total")
                 .rename(columns={"i": _renamed})
                 .set_index(_renamed)
                 , use_container_width=True)
    
    st.markdown('### Métricas')
    col1, col2, col3, col5 = st.columns(4)
    kpi_selected = col1.selectbox("Selecciona la métrica", 
                                  ["Current %"
                                   , "Current % (sin compras inventario o proveedor)"
                                   , "%IMORA"
                                   , "Delta %"
                                   , "Saldo OS+120 %"
                                   , "ROI"
                                   , "ROI ratio"
                                   , "ROI interes ratio"
                                   , "OS 8 mas %"
                                   , "OS 30 mas %"
                                   , "OS 60 mas %"
                                   , "OS 90 mas %"
                                   , "Roll 0 a 1"
                                #    , "Pérdida esperada"
                                   , "Pérdida esperada (saldo hasta 120 días)"
                                   , "Coincidential WO"
                                   , "Lagged WO"
                                   , "Total monto desembolsado"
                                   , "Saldo Total (sin castigos)"
                                   , "Saldo Total (con castigos)"
                                   , "Saldo Vencido"
                                   , "Monto promedio"
                                   , "Número de cuentas"
                                   , "Número de cuentas Activas"
                                   , "Número de cuentas Mora"
                                   , "Reestructuras %"
                                   , "Saldo mayor a 60 días"
                                   , "Cuentas en mora mayor a 60 días"
                                   , "Límite de crédito promedio"
                                   , "Días hasta la primera ampliación"
                                   ]
                                   +
                                   ["Métrica que necesito"]*("erick" in os.getcwd())
                                   )

    vista_selected = col2.selectbox("Selecciona la vista a desagregar:", 
                                   ["-- Sin vista --"
                                    , "Por tipo de corte"
                                    , "Por número de ampliaciones"
                                    , "Por zona"
                                    , "Por analista"
                                    , "Por estado de la tienda"
                                    , "Por edad del tiendero"
                                    , "Por rango de crédito"
                                    , "Por cohort"
                                    , "Por semestre de cohort"
                                    , "Por municipio"
                                    , "Por género del tiendero"
                                    , "Por giro del negocio"
                                    ])
    Promedio_comparar = col3.selectbox("Selecciona el promedio a comparar:"
                                       , ["Promedio YoFio", "Promedio sin la cartera seleccionada"])
    
           
    vista = {"Por tipo de corte": "term_type"
              , "Por zona": "ZONA"
              , "Por número de ampliaciones": "n_ampliaciones"
              , "Por analista": "Analista"
              , "Por edad del tiendero": "Edad"
              , "Por estado de la tienda": "Estado"
              , "Por cohort": "Fecha_apertura"
              , "Por semestre de cohort": "Semestre_cohort"
              , "Por rango de crédito": "Rango"
              , "Por municipio": "Municipio"
              , "Por género del tiendero": "genero_estimado"
              , "Por giro del negocio": "industry"
              , "-- Sin vista --": ""
             }[vista_selected]
    
    kpi = {"Current %": "porcentaje" 
            , "Current % (sin compras inventario o proveedor)": "porcentaje"
            , "%IMORA": "porcentaje"
            , "Delta %": "porcentaje"
            , "Saldo OS+120 %": "porcentaje"
            , "ROI": "dinero"
             , "OS 8 mas %": "porcentaje"
             , "OS 30 mas %": "porcentaje"
             , "OS 60 mas %": "porcentaje"
             , "OS 90 mas %": "porcentaje"
             , "Roll 0 a 1": "porcentaje"
             , "Pérdida esperada": "porcentaje"
             , "Pérdida esperada (saldo hasta 120 días)": "porcentaje"
             , "Coincidential WO": "porcentaje"
             , "Total monto desembolsado": "dinero"
             , "Lagged WO": "porcentaje"
             , "Saldo Total (sin castigos)": "dinero"
             , "Saldo Total (con castigos)": "dinero"
             , "Saldo Vencido": "dinero" 
             , "Monto promedio": "dinero"
             , "Número de cuentas": "cuentas"
             , "Número de cuentas Activas": "cuentas"
             , "Número de cuentas Mora": "cuentas"
             , "Reestructuras %": "porcentaje"
             , "Saldo mayor a 60 días": "dinero"
             , "Cuentas en mora mayor a 60 días": "cuentas"
             , "Límite de crédito promedio": "dinero"
             , "Días hasta la primera ampliación": "cuentas"
             , "Métrica que necesito": "cuentas"
             , "ROI ratio": "cuentas"
             , "ROI interes ratio": "cuentas"
             }[kpi_selected]

    kpi_task = {"Current %": current_pct_task 
                , "Current % (sin compras inventario o proveedor)": current_sin_ip_pct_task
                , "%IMORA": imora_task
                , "Delta %": delta_pct_task
                 , "Saldo OS+120 %": Default_rate_task
                 , "ROI": roi_task
                 , "ROI ratio": roi_ratio_task
                 , "ROI interes ratio": roi_interes_ratio_task
                 , "OS 8 mas %": os_8_task
                 , "OS 30 mas %": os_30_task
                 , "OS 60 mas %": os_60_task
                 , "OS 90 mas %": os_90_task
                 , "Roll 0 a 1": roll_0_1_task
                 , "Pérdida esperada": perdida_task
                 , "Pérdida esperada (saldo hasta 120 días)": perdida_hasta_120_task
                 , "Coincidential WO": coincidential_task
                 , "Lagged WO": lagged_task
                 , "Total monto desembolsado": total_amount_disbursed_task
                 , "Saldo Total (sin castigos)": OSTotal_sincastigos_task
                 , "Saldo Total (con castigos)": OSTotal_concastigos_task
                 , "Monto promedio": credit_limit
                 , "Saldo Vencido": SaldoVencido_task 
                 , "Número de cuentas": NumCuentas_task
                 , "Número de cuentas Activas": Activas_task
                 , "Número de cuentas Mora": Mora_task
                 , "Reestructuras %": reestructura_task
                 , "Saldo mayor a 60 días": os_60_monto_task
                 , "Cuentas en mora mayor a 60 días": os_60_cuentas_task
                 , "Límite de crédito promedio": lim_credito_avg_task
                #  , "Días hasta la primera ampliación": tiempo_hasta_primera_ampliacion_task
                 }
    if "erick" in os.getcwd():
        kpi_task["Métrica que necesito"] = metrica_task

    kpi_task = kpi_task[kpi_selected]
    
    kpi_des = {"Current %": "Saldo en Bucket_Current dividido entre Saldo Total (sin castigos)" 
               , "Current % (sin compras inventario o proveedor)": "Saldo en Bucket_Current sin incluir saldo de compras a proveedor o inventario dividido entre Saldo Total (sin castigos)"
               , "%IMORA": "Suma de últimos 12 deltas móviles dividido entre Saldo Total (sin castigos) más suma de últimos 12 deltas móviles."
               , "Delta %": "Saldo en bucket delta del mes multiplicado por 12 dividido entre Saldo Total (sin castigos) más suma de últimos 12 deltas móviles."
               , "Saldo OS+120 %": "Saldo a más de 120 días dividido entre Saldo Total (incluyendo castigos)"
               , "ROI": "Pagos a capital, interés y moratorios menos capital desembolsado"
               , "OS 8 mas %": "Saldo a más de 8 días de atraso dividido entre Saldo Total (sin castigos)"
               , "OS 30 mas %": "Saldo a más de 30 días de atraso dividido entre Saldo Total (sin castigos)"
               , "OS 60 mas %": "Saldo a más de 60 días de atraso dividido entre Saldo Total (sin castigos)"
               , "OS 90 mas %": "Saldo a más de 90 días de atraso dividido entre Saldo Total (sin castigos)"
               , "Roll 0 a 1": "Saldo rodado de bucket 0 a 1."
               , "Total monto desembolsado": "Monto desembolsado acumulado (desembolsos y compras)."
               , "Pérdida esperada": "Roll anualizado por saldo Current entre Saldo Total (incluyendo castigos). Valor probabilístico."
               , "Pérdida esperada (saldo hasta 120 días)": "Roll anualizado por saldo Current entre Saldo Total (sin incluir castigos). Valor probabilístico."
               , "Coincidential WO": "Bucket Delta dividido entre Saldo Total (sin castigos)"
               , "Lagged WO": "Bucket Delta dividido entre Saldo Total (sin castigos) de hace 5 períodos."
               , "Saldo Total (sin castigos)": "Saldo Total sin bucket 120"
               , "Saldo Vencido": "Saldo en status LATE"
               , "Saldo Total (con castigos)": "Saldo Total incluyendo bucket 120"
               , "Monto promedio": "Límite de crédito promedio."
               , "Número de cuentas": "Total cuentas colocadas (acumuladas)"
               , "Reestructuras %": "Porcentaje de cuentas reestructuradas sin considerar castigadas."
               , "Número de cuentas Activas": "Cuentas en CURRENT o LATE"
               , "Número de cuentas Mora": "Cuentas en LATE"
               , "Saldo mayor a 60 días": "Saldo mayor a 60 días (sin castigos)"
               , "Cuentas en mora mayor a 60 días": "Cuentas en mora mayor a 60 días (sin castigos)"
               , "Límite de crédito promedio": "Límite de crédito promedio"
               , "Días hasta la primera ampliación": "Días hasta la primera ampliación"
               , "ROI ratio": "Pagos a capital, interés y moratorios dividido entre capital desembolsado."
               , "ROI interes ratio": "Pagos a interés y moratorios dividido entre capital desembolsado."
              }
    if "erick" in os.getcwd():
        kpi_des["Métrica que necesito"] = ""

    kpi_des = kpi_des[kpi_selected]
    
    formateada, temp = format_column(temp, vista)
    formateada, YoFio = format_column(YoFio, vista)
    vista = vista + "_formato" * int(formateada)


    if vista == "":
        Cartera = kpi_task(temp, vista).assign(Vista="Cartera seleccionada")
    else: 
        Cartera = kpi_task(temp, vista).rename(columns={vista: "Vista"})



    
    if kpi in ("dinero", "cuentas"):

        to_plot = pd.concat([Cartera])

        fig1 = px.line(to_plot
                        , x="Fecha_reporte"
                        , y="Metric"
                        , color="Vista"
                       )

        if kpi in ("dinero"):
            fig1.layout.yaxis.tickformat = '$,'
        else:
            fig1.layout.yaxis.tickformat = ','
        if vista == "genero_estimado":
            fig1["data"][1]["line"]["color"] = "purple"
            fig1["data"][0]["line"]["color"] = "green"
            fig1["data"][2]["line"]["color"] = "pink"
    else:
        if Promedio_comparar == "Promedio YoFio":
            Promedio = kpi_task(YoFio, "").assign(Vista="Promedio YoFio")
        else:
            Promedio = (kpi_task(YoFio
                                 .merge(temp[["ID_Credito"]]
                                        .drop_duplicates()
                                        , how="left"
                                        , indicator=True
                                        )
                                 .query("_merge == 'left_only'")
                                 , "")
                        .assign(Vista="Promedio YoFio sin cartera seleccionada")
                        .sort_values(by="Fecha_reporte", ignore_index=True)
                       )
        to_plot = pd.concat([Promedio, Cartera])

        if kpi_selected == 'Pérdida esperada' and _cortes in ("Mensual", "Por mes"):
            # Calculate the moving average with a window size equal to 6 periods
            Promedio_ma = (Promedio
                           .assign(Metric = lambda df: df.Metric.rolling(window=6).mean()
                                    , Vista = "Promedio YoFio (MA)"
                                   )
                           .dropna()
                           .sort_values(by="Fecha_reporte", ignore_index=True)
                           )
            to_plot = pd.concat([to_plot, Promedio_ma])

        

        fig1 = px.line(to_plot
                        , x="Fecha_reporte"
                        , y="Metric"
                        , color="Vista"
                       )
        fig1["data"][0]["line"]["color"] = "black"
        if kpi_selected == 'Pérdida esperada' and _cortes in ("Mensual", "Por mes"):
            fig1["data"][2]["line"]["dash"] = "dash"
        if vista == "genero_estimado":
            fig1["data"][2]["line"]["color"] = "red"
            
        # Fill between 18% and 22% of the y-axis
        if kpi_selected == 'Pérdida esperada' and _cortes in ("Mensual", "Por mes"):
            fig1.update_layout(
                shapes=[
                    dict(
                        type= 'rect', 
                        xref= 'paper', 
                        yref= 'y', 
                        x0= 0, 
                        y0= 0.18, 
                        x1= 1, 
                        y1= 0.22,
                        fillcolor= 'LightSalmon',
                        opacity= 0.3,
                        layer= 'below', 
                        line_width= 0
                    )
                ]
            )
            # Set a legend for the fill between trace named "Apetito de riesgo"
            fig1.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=10, color='LightSalmon', opacity=0.3),
                showlegend=True,
                name=r"Apetito de riesgo 18% - 22%",
                hoverinfo='none'
            ))



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
    if zoom and not (kpi in ("dinero", "cuentas")):
        fig1.update_yaxes(range=[0, 1])

    st.plotly_chart(fig1
                    , use_container_width=True
                    , height = 450
                    , theme="streamlit"
                    )
    if "erick" in os.getcwd():
        st.dataframe(to_plot
                     .query("Fecha_reporte.isin(['2023-08-31', '2023-09-30']) and Vista != 'Promedio YoFio'")
                     .filter(["Vista", "Fecha_reporte", "Metric"])
                     .sort_values(by=["Vista", "Fecha_reporte"], ignore_index=True)
                     , width=500
                    )
    del fig1, Cartera, to_plot, csv_metricas, formateada, vista, kpi_des, zoom
    try:
        del Promedio
    except:
        pass










    #
    # ROLLS
    #
    st.markdown('### Rolls')
    _, _, _, _, _, _, d = st.columns(7)
    csv1 = convert_df(rolls_toplot
                      .filter(list(rolls_toplot)[3:][::-1])
                      .reset_index()
    )
    d.download_button(
        label="Descargar CSV",
        data=csv1,
        file_name='rolls.csv',
        mime='text/csv',
    )
    st.dataframe(rolls_toplot
                 .filter(list(rolls_toplot)[3:][::-1])
                 .reset_index()
                 .assign(Roll = lambda df: df.Roll.apply(lambda x: x.replace("Pérdida", "Pérdida < 120")))
                 .set_index("Roll")
                         
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
    
    fechas = ", ".join(["'%s'" % str(d)[:10] for d in pd.date_range("2020-01-31", periods=200, freq="M")])
    _query = " and ".join([f for f in filtro_BQ.split(" and ") if "Fecha_reporte" not in f])
    df_cosechas = (df_cosechas
                   .assign(Dias_de_atraso = lambda df: df.Dias_de_atraso.apply(lambda x: max(x, 0)))
                   .query("Fecha_reporte in (%s)" % (fechas))
                   .assign(Bucket_2 = lambda df: df.Dias_de_atraso.apply(Bucket_Monthly)
                           , Bucket_par8 = lambda df: df.Dias_de_atraso.apply(Bucket_Par8)
                           )
                   .rename(columns={"balance": "Saldo"})
                   .sort_values(by=["ID_Credito", "Fecha_reporte"], ignore_index=True)
                  )
     
    df_cosechas["t"] = df_cosechas.assign(t=range(len(df_cosechas))).groupby(["ID_Credito"]).t.rank()
    df_cosechas["Cosecha"] = df_cosechas.apply(lambda row: "M"+str(diff_month(row["Fecha_reporte"], str(row["Fecha_apertura"])[:7]+"-01" )).zfill(3), axis=1)
    df_cosechas["Mes_apertura"] = df_cosechas["Fecha_apertura"].apply(str).str[:7]
    fecha_reporte_max = df_cosechas.Fecha_reporte.sort_values().iloc[-1]
        
      
    df_cosechas = (df_cosechas
                  .merge(df_cosechas
                         .assign(t=lambda df: df.t+1)
                         [["ID_Credito", "Dias_de_atraso", "Fecha_reporte", "t"]]
                         , on=["ID_Credito", "t"]
                         , suffixes=("", "_ant")
                         , how="left")
                   .drop(columns=["t", "Fecha_reporte_ant"])
                  
                 )
    metricas_cosechas = {"Saldo Total (incluyendo castigos)": "Saldo"
                           , "Saldo Total (sin castigos)": "Saldo_no_castigado"
                           , "Saldo castigado (+120 dpd)": "Saldo_castigado"
                           , "Total compras colocadas (Acumulado)": "Monto_compra_acumulado"
                           , "Total colocado (Acumulado)": "Total_colocado_acumulado"
                           , "Número de cuentas (incluyendo castigos)": "Creditos"
                           , "Número de cuentas (sin castigos)": "Creditos_no_castigados"
                           , "Cuentas activas": "cuentas_activas"
                           , "% IMORA": "IMORA"
                           , "Par 8": "Par8"
                           , "Par 30": "Par30"
                           , "Par 60": "Par60"
                           , "Par 90": "Par90"
                           , "Par 120": "Par120"
                        }
    
    _a, _, _ = st.columns(3)
    metrica_cosecha = _a.selectbox("Selecciona métrica:"
                                   , metricas_cosechas.keys()
                                   )
    metrica_seleccionada = metricas_cosechas[metrica_cosecha]
    # st.dataframe(df_cosechas)
    if metrica_seleccionada == "Saldo" or metrica_seleccionada == "IMORA":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Saldo"].copy()
    elif metrica_seleccionada == "Saldo_no_castigado":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Saldo"]*(df_cosechas["Dias_de_atraso"] < 120).astype(int)
    elif metrica_seleccionada == "Saldo_castigado":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Saldo"]*(df_cosechas["Dias_de_atraso"] >= 120).astype(int)
    elif metrica_seleccionada == "Monto_compra_acumulado":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Monto_compra_acumulado"].copy()
    elif metrica_seleccionada == "Total_colocado_acumulado":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Monto_compra_acumulado"] + df_cosechas["amount_disbursed"]
    elif metrica_seleccionada == "cuentas_activas":
        df_cosechas["Metrica seleccionada"] = ((df_cosechas["Dias_de_atraso"] < 120) & (df_cosechas["Status_credito"] != "I")).astype(int)
    elif metrica_seleccionada == "Creditos":
        df_cosechas["Metrica seleccionada"] = 1
    elif metrica_seleccionada == "Creditos_no_castigados":
        df_cosechas["Metrica seleccionada"] = (df_cosechas["Dias_de_atraso"] < 120).astype(int)
    elif metrica_seleccionada == "Par8":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Saldo"]*((df_cosechas["Dias_de_atraso"] >= 8) & (df_cosechas["Dias_de_atraso"] < 120)).astype(int)
    elif metrica_seleccionada == "Par30":
        st.write("Par30")
        df_cosechas["Metrica seleccionada"] = df_cosechas["Saldo"]*((df_cosechas["Dias_de_atraso"] >= 30) & (df_cosechas["Dias_de_atraso"] < 120)).astype(int)
    elif metrica_seleccionada == "Par60":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Saldo"]*((df_cosechas["Dias_de_atraso"] >= 60) & (df_cosechas["Dias_de_atraso"] < 120)).astype(int)
    elif metrica_seleccionada == "Par90":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Saldo"]*((df_cosechas["Dias_de_atraso"] >= 90) & (df_cosechas["Dias_de_atraso"] < 120)).astype(int)
    elif metrica_seleccionada == "Par120":
        df_cosechas["Metrica seleccionada"] = df_cosechas["Saldo"]*(df_cosechas["Dias_de_atraso"] >= 120).astype(int)

    if metrica_seleccionada == 'IMORA':
        Cosechas = (imora_task(temp, "Fecha_apertura")
                    .assign(Mes_apertura = lambda df: df.Fecha_apertura.apply(str).str[:7])
                    .assign(F = lambda df: df.Mes_apertura.apply(lambda x: int(x.replace("-","")) >= 202108))
                    .query("F")
                    .drop(columns="F")
                    .assign(Cosecha = lambda df: "M"+df.apply(lambda row: diff_month(row.Fecha_reporte, row.Mes_apertura+"-01"), axis=1).astype(str).str.zfill(3))
                    .filter(["Mes_apertura", "Cosecha", "Metric"])
                   )
        formato = lambda x: "{:,.2f}%".format(x*100) if x == x else ""
        

    else:
        Cosechas = (df_cosechas
                    .groupby(["Mes_apertura", "Cosecha"], as_index=False)
                    .agg(Metric = pd.NamedAgg("Metrica seleccionada", "sum"))

                )
        if metrica_seleccionada != "cuentas_activas":
            Cosechas = Cosechas[Cosechas["Mes_apertura"].apply(lambda x: int(x.replace("-","")) >= 202108)]

        formato = (lambda x: "${:,.0f}".format(x) if x == x else x) if "cuentas" not in metrica_cosecha.lower() else (lambda x: "{:,.0f}".format(x) if x == x else x)


        
        
    # st.dataframe(Cosechas)

    
    Cosechas_toshow = (Cosechas
                       .pivot(index="Mes_apertura"
                              , columns="Cosecha"
                              , values="Metric"
                             )
                       )

    Cosechas_toshow = (Cosechas_toshow
                       .applymap(formato)
                       .fillna("")
                       )
    

    
    Cosechas = Cosechas.filter(['Mes_apertura', 'Cosecha', 'Saldo', 'Creditos'])
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
                           , values="Metrica seleccionada"
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



    tb1, tb2 = st.tabs(["Matriz cosechas", "Cosechas por buckets"])

    with tb1:
        _, _, _, _d = st.columns(4)
        csv2 = convert_df(Cosechas_toshow
                          .applymap(lambda x: x.replace("%", "").replace("$", "").replace(",", "") if isinstance(x, str) else x)
                          .reset_index()
                         )
        _d.download_button(
            label="Descargar CSV",
            data=csv2,
            file_name='cosechas.csv',
            mime='text/csv',
        )
        st.dataframe(Cosechas_toshow
                    , height=666
                    , use_container_width=True)


    with tb2:
        Cosecha_dropdown = list(df_agg.Cosecha.unique())
        Cosecha_dropdown.sort()
        st.markdown("##### Cosechas desagregadas por bucket")
        k1, _, k5 = st.columns(3)
        Cosecha_selected = k1.selectbox("Selecciona una cosecha:"
                                        , Cosecha_dropdown
                                        )

        vista_calendario = st.checkbox("¿Vista meses calendario?", value=False)

    
        if "erick" in os.getcwd():
            csv3 = convert_df(df_agg
                              .assign(Bucket = lambda df: df["Bucket"].apply(lambda x: "6. WO (delta)" if "WO" in x else x))
                              .melt(id_vars=["Cosecha", "Bucket"]
                                    , var_name="MOB"
                                    , value_name="Value"
                                   )
                             )
        else:
            csv3 = convert_df(df_agg[df_agg.Cosecha == Cosecha_selected].assign(Bucket = lambda df: df["Bucket"].apply(lambda x: "6. WO (delta)" if "WO" in x else x)))

        
        k5.download_button(
            label="Descargar CSV",
            data=csv3,
            file_name='Cosecha_Bucket_%s.csv' % Cosecha_selected,
            mime='text/csv'
        )
        def _formato(x, metrica_seleccionada):
            if metrica_seleccionada in ("Saldo", "Saldo_no_castigado", "Saldo_castigado"):
                return "${:,.0f}".format(x)
            elif "cuentas" in metrica_seleccionada.lower() or "creditos" in metrica_seleccionada.lower():
                return "{:,.0f}".format(x)

        df_agg = (df_agg
                [df_agg.Cosecha == Cosecha_selected]
                .applymap(lambda x: _formato(x, metrica_seleccionada) if not isinstance(x, str) else x)
                .assign(Bucket = lambda df: df["Bucket"].apply(lambda x: "6. WO (delta)" if "WO" in x else x))
                .reset_index(drop=True)
                .set_index(["Cosecha", "Bucket"])
                )
        
        _fechas = pd.date_range(Cosecha_selected+"-01", periods=120, freq="M")
        _fechas = [str(f)[:7] for f in _fechas if str(f)[:10] <= fecha_reporte_max]
        _fechas = {"M"+str(i).zfill(3): fecha for i, fecha in enumerate(_fechas)}

        if vista_calendario:
            df_agg = df_agg.rename(columns=_fechas).filter(list(_fechas.values()))
        else:
            df_agg = df_agg.filter(list(_fechas.keys()))

        st.dataframe(df_agg, use_container_width=True)
    
    
 
    

    st.subheader("Métricas de riesgo por cohort")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Par 8", "Par 30", "Par 120", "ROI ratio", "KPIS por cohort"])

    with tab1:
        st.markdown("### Par 8")
        
        to_plot_par8 = os_8_task(temp.query("Fecha_apertura >= '2021-08'"), "Fecha_apertura")
        to_plot_par8['Mes'] = to_plot_par8.apply(lambda x: "M" + str(diff_month(x['Fecha_reporte'], x['Fecha_apertura']+"-01")).zfill(3), axis=1)

        promedio_par30 = os_8_task(YoFio.query("Fecha_apertura >= '2021-08'"), "Mes")

        to_plot_par8 = (pd.concat([to_plot_par8, promedio_par30.assign(Fecha_apertura = "Promedio General")])
                         .rename(columns={"Fecha_apertura": "Cosecha"})
                         .sort_values(by=["Mes", "Cosecha"]
                                      , ascending=[True, True]
                                      , ignore_index=True)
                        ) 

        _, _, _, _, _, _, d = st.columns(7)
        csv4 = convert_df(to_plot_par8.pivot_table(index=["Mes"], columns=["Cosecha"], values="Metric").fillna("") )
        d.download_button(
            label="Descargar CSV",
            data=csv4,
            file_name='par8.csv',
            mime='text/csv'
        )
        st.write("Doble click en la leyenda para aislar")

        fig3 = px.line(to_plot_par8
                    , x="Mes"
                    , y="Metric"
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
    with tab2:
        st.markdown("### Par 30")
        flag_WO = st.checkbox("Incluir WO")

        par30_df = os_30_task(temp.query("Fecha_apertura >= '2021-08'"), "Fecha_apertura")
        temp["Mes"] = temp.apply(lambda x: "M" + str(diff_month(x['Fecha_reporte'], x['Fecha_apertura']+"-01")).zfill(3), axis=1)
        par30_df["Mes"] = par30_df.apply(lambda x: "M" + str(diff_month(x['Fecha_reporte'], x['Fecha_apertura']+"-01")).zfill(3), axis=1)

        par30_df_WO = os_30_task_con_WO(temp.query("Fecha_apertura >= '2021-08'"), "Fecha_apertura")
        par30_df_WO["Mes"] = par30_df_WO.apply(lambda x: "M" + str(diff_month(x['Fecha_reporte'], x['Fecha_apertura']+"-01")).zfill(3), axis=1)

        to_plot_par30 = par30_df_WO.copy() if flag_WO else par30_df.copy()

        promedio_par30_df = os_30_task(YoFio.query("Fecha_apertura >= '2021-08'"), "Mes").assign(Fecha_apertura = "Promedio General")
        promedio_par30_df_WO = os_30_task_con_WO(YoFio.query("Fecha_apertura >= '2021-08'"), "Mes").assign(Fecha_apertura = "Promedio General")

        promedio_par30 = promedio_par30_df_WO.copy() if flag_WO else promedio_par30_df.copy()

        to_plot_par30 = (pd.concat([to_plot_par30, promedio_par30])
                         .rename(columns={"Fecha_apertura": "Cosecha"})
                         .sort_values(by=["Mes", "Cosecha"]
                                      , ascending=[True, True]
                                      , ignore_index=True)
                        ) 

        _, _, _, _, _, isra, d = st.columns(7)

        # st.markdown(", ".join(temp.columns))
        
        # isra.download_button(
        #     label="Descargar CSV Isra",
        #     data=convert_df(temp
        #                     .filter(["ID_Credito", "Fecha_apertura", "Mes", "balance_sin_ip", "Bucket"])
        #                     .rename(columns={"balance_sin_ip": "balance"})
        #                     .merge(pd.read_csv("Data/cat_ID_Credito.csv")
        #                            , how="left"
        #                            , on="ID_Credito"
        #                            )
        #                    ),
        #     file_name='isra.csv',
        #     mime='text/csv'
        # )
        csv5 = convert_df(to_plot_par30.pivot_table(index=["Mes"], columns=["Cosecha"], values="Metric").fillna(""))
        d.download_button(
            label="Descargar CSV",
            data=csv5,
            file_name='par30.csv',
            mime='text/csv'
        )
        st.write("Doble click en la leyenda para aislar")
        
        fig3 = px.line(to_plot_par30
                    , x="Mes"
                    , y="Metric"
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
        
        l1, _, _, _, _ = st.columns(5)
        Mob_selected = l1.selectbox("Selecciona el Mob:"
                                        , [str(i).zfill(2) for i in range(1,13)]
                                        , key="Mob_selected par 30"
                                        , index=2
                                        )
        
        st.markdown("### Zoom Par 30 Mob %i" % int(Mob_selected))
        
        Par30Mob3 = (to_plot_par30
                    .query("Mes == 'M0%s'" % Mob_selected)
                    .sort_values(by=["Metric"]
                                , ascending=[False]
                                , ignore_index=True
                                )
                    .assign(Cosecha = lambda df: df.Cosecha.apply(lambda x: "Promedio" if "Promedio" in x else str(x))
                            , color = lambda df: df.Cosecha.apply(lambda x: "red" if "Promedio" in x else 'blue')

                            )
                    )
        Par30Mob3['category'] = [str(i) for i in Par30Mob3.index]
        
        
        fig4 = px.bar(Par30Mob3
                    , y='Metric'
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
        
    with tab3:
        st.markdown("### Par 120")
        
        to_plot_par120 = Default_rate_task(temp.query("Fecha_apertura >= '2021-08'"), "Fecha_apertura")
        to_plot_par120['Mes'] = to_plot_par120.apply(lambda x: "M" + str(diff_month(x['Fecha_reporte'], x['Fecha_apertura']+"-01")).zfill(3), axis=1)

        promedio_par120 = Default_rate_task(YoFio.query("Fecha_apertura >= '2021-08'"), "Mes")

        to_plot_par120_ = (pd.concat([to_plot_par120, promedio_par120.assign(Fecha_apertura = "Promedio General")])
                         .rename(columns={"Fecha_apertura": "Cosecha"})
                         .sort_values(by=["Mes", "Cosecha"]
                                      , ascending=[True, True]
                                      , ignore_index=True)
                        ) 

        _, _, _, _, _, _, dd = st.columns(7)
        csv6 = convert_df(to_plot_par120_.pivot_table(index=["Mes"], columns=["Cosecha"], values="Metric").fillna(""))
        dd.download_button(
            label="Descargar CSV",
            data=csv6,
            file_name='par120.csv',
            mime='text/csv'
        )
        st.write("Doble click en la leyenda para aislar")
        
        fig4 = px.line(to_plot_par120_
                    , x="Mes"
                    , y="Metric"
                    , color="Cosecha"
                    )
        fig4.update_traces(line=dict(width=0.8))
        
        
        
        for i in range(len(fig4['data'])):
            if fig4['data'][i]['legendgroup'] == 'Promedio General':
                fig4['data'][i]['line']['color'] = 'black'
                fig4['data'][i]['line']['width'] = 1.2
            if fig4['data'][i]['legendgroup'] == '2022-05':
                fig4['data'][i]['line']['color'] = 'brown'
        
        
        
        fig4.layout.yaxis.tickformat = ',.1%'
        fig4.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')
        
        
        st.plotly_chart(fig4
                        , use_container_width=True
        )

        m1, _, _, _, _ = st.columns(5)
        Mob_selected = m1.selectbox("Selecciona el Mob:"
                                        , [str(i).zfill(2) for i in range(1,13)]
                                        , key="Mob_selected par 120"
                                        , index=11
                                        )
        
        st.markdown("### Zoom Par 120 Mob %i" % int(Mob_selected))

        Par120Mob3 = (to_plot_par120_
                      .query("Mes == 'M0%s'" % Mob_selected)
                        .sort_values(by=["Metric"]
                                    , ascending=[False]
                                    , ignore_index=True
                                    )
                        .assign(Cosecha = lambda df: df.Cosecha.apply(lambda x: "Promedio" if "Promedio" in x else str(x))
                                , color = lambda df: df.Cosecha.apply(lambda x: "red" if "Promedio" in x else 'blue')

                                )
                        )

        Par120Mob3['category'] = [str(i) for i in Par120Mob3.index]

        fig8 = px.bar(Par120Mob3
                    , y='Metric'
                    , x='Cosecha'
                    , color="category"
                    , color_discrete_sequence=list(Par120Mob3["color"].values)
                    , text_auto=',.1%'
                    )
        fig8.layout.yaxis.tickformat = ',.1%'
        fig8.layout.xaxis.type = 'category'
        fig8.update_traces(textfont_size=12
                        , textangle=0
                        , textposition="inside"
                        , cliponaxis=False
                        )
        fig8.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')
        st.plotly_chart(fig8
                        , use_container_width=True
                        , height = 450
                        , theme="streamlit"
                        )


    with tab4:
        st.markdown("### ROI ratio")
        _d_, _, _, _, d = st.columns(5)

        metric = _d_.selectbox("Selecciona métrica:"
                              , ["ROI ratio", "ROI interes ratio"]
                              )
        if metric == "ROI ratio":
            to_plot_roi = roi_ratio_task(temp.query("Fecha_apertura >= '2021-08'"), "Fecha_apertura")
            to_plot_roi['Mes'] = to_plot_roi.apply(lambda x: "M" + str(diff_month(x['Fecha_reporte'], x['Fecha_apertura']+"-01")).zfill(3), axis=1)
            promedio_roi = roi_ratio_task(YoFio.query("Fecha_apertura >= '2021-08'"), "Mes")
        elif metric == "ROI interes ratio":
            to_plot_roi = roi_interes_ratio_task(temp.query("Fecha_apertura >= '2021-08'"), "Fecha_apertura")
            to_plot_roi['Mes'] = to_plot_roi.apply(lambda x: "M" + str(diff_month(x['Fecha_reporte'], x['Fecha_apertura']+"-01")).zfill(3), axis=1)
            promedio_roi = roi_interes_ratio_task(YoFio.query("Fecha_apertura >= '2021-08'"), "Mes")

        to_plot_roi_ = (pd.concat([to_plot_roi, promedio_roi.assign(Fecha_apertura = "Promedio General")])
                            .rename(columns={"Fecha_apertura": "Cosecha"})
                            .sort_values(by=["Mes", "Cosecha"]
                                        , ascending=[True, True]
                                        , ignore_index=True)
                            )

        
        csv7 = convert_df(to_plot_roi_.pivot_table(index=["Mes"], columns=["Cosecha"], values="Metric").fillna(""))
        d.download_button(
            label="Descargar CSV",
            data=csv7,
            file_name='roi.csv',
            mime='text/csv'
        )
        if metric == "ROI ratio":
            st.write("Pagos a capital, intereses y moratorios dividido entre capital desembolsado. La línea punteada azul representa el retorno positivo. ")
        elif metric == "ROI interes ratio":
            st.write("Pagos a intereses y moratorios dividido entre capital desembolsado. La línea punteada azul representa el retorno positivo. ")
        st.write("(Doble click en la leyenda para aislar)")

        fig7 = px.line(to_plot_roi_.rename(columns={"Mes": "MOB"})
                    , x="MOB"
                    , y="Metric"
                    , color="Cosecha"
                    )
        fig7.update_traces(line=dict(width=0.8))

        for i in range(len(fig7['data'])):
            if fig7['data'][i]['legendgroup'] == 'Promedio General':
                fig7['data'][i]['line']['color'] = 'black'
                fig7['data'][i]['line']['width'] = 1.2
            if fig7['data'][i]['legendgroup'] == '2022-05':
                fig7['data'][i]['line']['color'] = 'brown'

        fig7.layout.yaxis.tickformat = ',.2'
        fig7.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')

        if metric == "ROI ratio":
            # Add a horizontal line at y=1 to represent the break-even point
            fig7.add_shape(type="line"
                        , x0=0
                        , x1=len(to_plot_roi_.Mes.unique())
                        , y0=1
                        , y1=1
                        , line=dict(color="darkblue", width=1, dash="dash"))

        st.plotly_chart(fig7, use_container_width=True, height = 450, theme="streamlit")







    with tab5:
        st.markdown("### KPIs por cohort")
        n1, _, _, _, _ = st.columns(5)

        cohort_sel = n1.selectbox("Selecciona el cohort:"
                                  , ["Promedio General"] + list(df_cosechas.Mes_apertura.drop_duplicates().sort_values(ignore_index=True).values)[5:]
                                  , key="cohort_sel"
                                  )
        
        flag_kpis = st.checkbox("Filtrar hasta 2022-08")
        if flag_kpis:
            promedio_par30_df = os_30_task(YoFio.query("Mes >= '2021-08' and Mes <= '2022-08'"), "Mes").assign(Fecha_apertura = "Promedio General")
            promedio_par30_df_WO = os_30_task_con_WO(YoFio.query("Mes >= '2021-08' and Mes <= '2022-08'"), "Mes").assign(Fecha_apertura = "Promedio General")
            promedio_par120 = Default_rate_task(YoFio.query("Mes >= '2021-08' and Mes <= '2022-08'"), "Mes")

            to_plot_par120_ = (pd.concat([to_plot_par120, promedio_par120.assign(Fecha_apertura = "Promedio General")])
                            .rename(columns={"Fecha_apertura": "Cosecha"})
                            .sort_values(by=["Mes", "Cosecha"]
                                        , ascending=[True, True]
                                        , ignore_index=True)
                            ) 


        to_plot = (pd.concat([par30_df, promedio_par30_df])
                   .drop(columns="Fecha_reporte")
                   .rename(columns={"Metric": "Par30"})
                   .merge(pd.concat([par30_df_WO, promedio_par30_df_WO])
                          .drop(columns="Fecha_reporte")
                          .rename(columns={"Metric": "Par30_WO"})
                          , on=["Mes", "Fecha_apertura"]
                          , how="left"
                         )
                    .rename(columns={"Fecha_apertura": "Cosecha"})
                    .merge(to_plot_par120_
                           .drop(columns="Fecha_reporte")
                           .rename(columns={"Metric": "Par120"})
                           , on=["Mes", "Cosecha"]
                           , how="left"
                          )
                    .melt(id_vars=["Mes", "Cosecha"]
                             , var_name="Metric"
                             , value_name="Value"
                             , ignore_index=True
                            )
                    
                    
                   )
        
        fig9 = px.line(to_plot
                       .query("Cosecha == '%s'" % cohort_sel)

                       , x="Mes"
                       , y="Value"
                       , color="Metric"
                      )
        fig9.layout.yaxis.tickformat = ',.0%'
        fig9.update_yaxes(showgrid=True, gridwidth=1, gridcolor='whitesmoke')
        fig9.update_layout(
            xaxis_title="Mes"
            , yaxis_title="Porcentaje"
        )
        fig9.update_layout(
            title={
                'text': "KPIs "+cohort_sel
                , 'y':0.9
                , 'x':0.5
                , 'xanchor': 'center'
                , 'yanchor': 'top'}
        )
        if "erick" in os.getcwd():
            csv9 = convert_df(to_plot)
        else:
            csv9 = convert_df(to_plot.query("Cosecha == '%s'" % cohort_sel))

        _, _, _, _, _, _, ff = st.columns(7)
        ff.download_button(
            label="Descargar CSV",
            data=csv9,
            file_name='pares %s.csv' % cohort_sel,
            mime='text/csv'
        )
        
        st.plotly_chart(fig9
                        , use_container_width=True
                        , height = 450
                        , theme="streamlit"
                        )



    
