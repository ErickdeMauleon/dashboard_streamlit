#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as _pd



class _PostgresHook:
    def __init__(self, postgres_conn_id):
        self.postgres_conn_id = postgres_conn_id
        
    def get_pandas_df(self, sql):
        import dotenv
        import os
        from sqlalchemy import create_engine
        
        if dotenv.load_dotenv("../../Credentials/.env"):
            if self.postgres_conn_id == 'postgres_yofio_prod':
                dbstring = "postgresql://%s:%s@%s:%s/%s" % (os.environ["USERPROD"]
                                                            , os.environ["PASSWORDPROD"]
                                                            , os.environ["HOSTPROD"]
                                                            , os.environ["PORTPROD"]
                                                            , os.environ["DBNAMEPROD"]
                                                           )
            elif self.postgres_conn_id == 'postgres_yofio_inventory':
                dbstring = "postgresql://%s:%s@%s:%s/%s" % (os.environ["USERBREF"]
                                                            , os.environ["PASSWORDBREF"]
                                                            , os.environ["HOSTBREF"]
                                                            , os.environ["PORTBREF"]
                                                            , os.environ["DBNAMEBREF"]
                                                           )
            else:
                raise
                
        connection = create_engine(dbstring).connect()
        _df = _pd.read_sql_query(sql, con=connection)
        return _df
    


# In[ ]:





# In[2]:


def tabla_genero():
    
    def get_genero(x):
        x = str(x)
        if len(x) > 10:
            if x[10] in ('H', 'M'):
                return x[10]
            else:
                return None
        else:
            return None

    def quitar_acentos(s):
        _a, _b = 'áéíóúü','aeiouu'
        _a += _a.upper()
        _b += _b.upper()
        _acentos = str.maketrans(_a, _b)

        return s.translate(_acentos)

    def prob_M(row):
        if str(row["nombre"]) in ('Sofia', 'Ileana', 'Tanya', 'Artemisa', 'Oralia'):
            return 1
        else:
            return round(row["M"]/(row["H"] + row["M"] + 0.0000001), 2)

    def prob_H(row):
        if str(row["nombre"]) in ('Cecilio'):
            return 1
        else:
            return round(row["H"]/(row["H"] + row["M"] + 0.0000001), 2)

    def estimar_genero(row):
        if row.prob_H == 0 and row.prob_M == 0:
            return None
        elif row.prob_H > row.prob_M:
            return 'H'
        elif row.prob_H < row.prob_M:
            return 'M'
        else:
            return None
    
    pg_hook = _PostgresHook(postgres_conn_id='postgres_yofio_prod')
    
    _query = """
    SELECT      CAST(account_shopkeeper_id AS varchar) AS account_id
                , name AS nombre
                , personhood_id AS genero
    FROM        shopkeeper
    """
    YoFio = (
        pg_hook.get_pandas_df(_query)
        .assign(nombre = lambda df: df["nombre"].apply(quitar_acentos).str.split(" ")
                , P = 1
                , genero = lambda df: df["genero"].apply(get_genero)
               )
    )
    
    temp = YoFio.explode("nombre")

    temp = (
        temp
        .merge(temp
               .fillna({"genero": "V"})
               .groupby(["nombre", "genero"])
               .agg({"P": "sum"})
               .reset_index()
               .pivot(index="nombre"
                      , columns="genero"
                      , values="P"
                     )
               .reset_index()
               .fillna(0)
               .assign(prob_H = lambda df: df.apply(prob_H, 1)
                       , prob_M = lambda df: df.apply(prob_M, 1)
                      )
               .filter(["nombre", "prob_H", "prob_M"])
               , how="left"
              )
        .groupby(["account_id"])
        .agg({"prob_H": "max"
              , "prob_M": "max"
             })
        .reset_index()
        .assign(genero_estimado = lambda df: df.apply(estimar_genero, 1))
        .filter(["account_id", "genero_estimado"])
        .merge(YoFio[["account_id", "nombre", "genero"]])
        .assign(genero_estimado = lambda df: df.genero.combine_first(df.genero_estimado))
        .query("genero_estimado == genero_estimado")
        .filter(["account_id", "genero_estimado"])
    )

    return temp


# In[3]:


genero_estimado = tabla_genero()

