import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import warnings
from datetime import datetime, date, timedelta
from dateutil import relativedelta
from st_pages import show_pages_from_config, add_page_title
from PIL import Image

url = "https://v.fastcdn.co/u/c2e5d077/58473217-0-Logo.png"
img = Image.open(requests.get(url, stream=True).raw)

st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title="PnL por Analista", page_icon=img)
add_page_title()

show_pages_from_config()


warnings.filterwarnings('ignore')
# Functions
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

# style for dataframes
th_props = [
  ('font-size', '14px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#F0F2F6')
  ]
                               
td_props = [
  ('font-size', '12px')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]


response = requests.get("https://raw.githubusercontent.com/ErickdeMauleon/data/main/style.css")
style_css = response.text

st.markdown(f'<style>{style_css}</style>', unsafe_allow_html=True)

def categorize_bucket(bucket):
    if bucket in ['BUCKET_ZERO', 'BUCKET_CURRENT']:
        return 'Reservas current'
    elif bucket in ['BUCKET_1_7', 'BUCKET_8_14', 'BUCKET_15_29']:
        return 'Reservas 1 a 29'
    elif bucket == 'BUCKET_30_59':
        return 'Reservas 30 a 59'
    elif bucket == 'BUCKET_60_89':
        return 'Reservas 60 a 89'
    else:
        return 'Reservas 90+'





def last_day_of_month(any_day):
    any_day = pd.to_datetime(any_day)
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return str(next_month - timedelta(days=next_month.day))[:10]



data = pd.read_csv("Data/PnL_Analistas.csv")
data['bucket_category'] = data['bucket'].apply(categorize_bucket)

pagos = pd.read_csv("Data/pagos_por_analista.csv")

# Sidebar filters
st.sidebar.title("Filtros")

advisors_list = list(data["advisor_name"].unique()) 
advisors_list.sort()
analista_selected = st.sidebar.multiselect("Selecciona el analista", ["Todos"] + advisors_list, default="Todos")

zone_list = list(data["zone"].unique())
zone_list.sort()
zone = st.sidebar.multiselect("Selecciona la zona", ["Todas"] + zone_list, default="Todas")

# Filter dataframes
if "Todos" not in analista_selected:
    data = data[data["advisor_name"].isin(analista_selected)]
    pagos = pagos[pagos["advisor_name"].isin(analista_selected)]

if "Todas" not in zone:
    data = data[data["zone"].isin(zone)]
    pagos = pagos[pagos["zone"].isin(zone)]

st.title("PnL por analista")
st.subheader("Tabla de factor de reserva")
_df = (pd.DataFrame({"Bucket": ["Reservas current", "Reservas 1 a 29", "Reservas 30 a 59", "Reservas 60 a 89", "Reservas 90+"]
                    , "Factor": ["{:.2%}".format(x) for x in [0.01, 0.3, 0.5, 0.75, 1]]})
       .set_index("Bucket")
       )

st.dataframe(_df.style.set_table_styles(styles))
st.subheader("Resumen de ingresos y gastos")
# st.dataframe(pagos
#              .groupby(["advisor_name", "Fecha_reporte"])
#              .agg(N = ("principal_invetory", "count"))
#              .reset_index()
#              .pivot(index = "advisor_name", columns = "Fecha_reporte", values = "N")
#              )
x = (data
     .assign(Fecha_reporte = lambda _df: _df["Fecha_reporte"].apply(last_day_of_month))
         .groupby(["Fecha_reporte"])
         .agg({"account_id": "sum"
               , "balance_current": "sum"
               , "balance_total": "sum"
               , "balance": "sum"
               , "saldo_reservado": "sum"
               })
        .join(pagos
              .assign(Fecha_reporte = lambda _df: _df["Fecha_reporte"].apply(last_day_of_month))
                .groupby(["Fecha_reporte"])
                .agg(Ingreso_Capital = ("principal_invetory", "sum")
                     , Ingreso_Interes = ("interest", "sum")
                     , Ingreso_interes_mora = ("late_interest", "sum")
                )
                )
        .assign(Ingreso_comisiones = ""
                , Total_Ingresos = lambda _df: _df["Ingreso_Interes"] + _df["Ingreso_interes_mora"] #+ _df["Ingreso_comisiones"]
                , balance_current = lambda _df: (_df["balance_current"] / (_df["balance_total"] + 0.0001)).apply(lambda x: f"{x:.2%}")
                )

         .assign(saldo_reservado_anterior=lambda _df: _df["saldo_reservado"] - _df["saldo_reservado"].shift(1)
                 , account_id=lambda _df: _df["account_id"].apply(lambda x: f"{x:,.0f}")

                 )
         .rename(columns={"account_id": "Número de cuentas activas"
                            , "balance": "Saldo Capital"
                            , "saldo_reservado": "Reserva cartera"
                            , "balance_current": "Current % (Saldo)"
                          , "Ingreso_Capital": "Ingreso de capital pagado"
                          , "Ingreso_Interes": "Ingreso de intereses pagados"
                          , "Ingreso_interes_mora": "Ingreso de moratorios pagados"
                          , "Ingreso_comisiones": "Ingreso de comisiones pagadas"
                          , "Total_Ingresos": "Total de ingresos (I)"
                          , "saldo_reservado_anterior": "Gasto de reserva del mes"
                          })
         .drop(columns=["balance_total"])
         .transpose()
         
         )

z = (data
     .groupby(["bucket_category", "Fecha_reporte"])
     .agg({"saldo_reservado": "sum"})

     .reset_index()
     .pivot(index="bucket_category", columns="Fecha_reporte", values="saldo_reservado")
     .fillna(0)
     )


y = z.copy()

meses = list(y.columns)
meses.sort()

for i in range(len(meses)):
    if i == 0:
        y[meses[i]] = z[meses[i]]
    else:
        y[meses[i]] = z[meses[i]] - z[meses[i-1]]



final = pd.concat([x
                   , y.loc[["Reservas current"]]
                   , y.iloc[:-1]
                   , (x.loc[["Saldo Capital"]]*0.015).rename(index={"Saldo Capital": "Costo de fondeo"})
                  ]
                  , axis=0)
final.loc["Incentivo variable"] = ""

# Gasto reserva del mes + Costo de fondeo + Incentivo variable
final.loc["Total gasto variable (II)"] = final.loc["Gasto de reserva del mes"] + final.loc["Costo de fondeo"]# + final.loc["Incentivo variable"]

# Total de ingresos - Total gasto variable
final.loc["Margen bruto (I - II)"] = final.loc["Total de ingresos (I)"] - final.loc["Total gasto variable (II)"]

csv0 = convert_df(final.assign(Analista = ", ".join(analista_selected)).reset_index().rename(columns={"index": "Indicador"}).filter(["Analista", "Indicador"] + final.columns.tolist()))
_, _, _, _, _, b6 = st.columns(6)
b6.download_button(label="Descargar CSV"
                   , data=csv0
                  , file_name='PnL_analista.csv'
                  , mime='text/csv'
                  )

st.table(final
         .drop(columns=["2022-11-30"], errors="ignore")
         .fillna("")
         .applymap(lambda x: f"${x:,.0f}" if isinstance(x, str) == False else x)
         .style.set_table_styles(styles)
         )



