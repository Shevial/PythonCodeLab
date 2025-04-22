import pandas as pd
from django.db import connection

# Aquí se va a extraer la información de la base de datos y se va a mostrar en un dataframe
# Se pueden implementar aquí las consultas de Pandas
def mostrar_dataframe():

   querytablas = "SHOW TABLES"
   dftables = pd.read_sql_query(querytablas, con=connection)
   print(dftables)

   query_ont = "SELECT * FROM ftth_ont"
   df_ont = pd.read_sql_query(query_ont, con=connection)
   print("Datos de la tabla ftth_ont:")
   print(df_ont)

   query_cliente = "SELECT * FROM crm_cliente"
   df_cliente = pd.read_sql_query(query_cliente, con=connection)
   # df_cliente.to_excel("C:/Users/User/Downloads/clientes.xlsx", index=False)
   print("Datos de la tabla crm_cliente:")
   print(df_cliente)

   # queryjoin = """
   #    SELECT *
   #    FROM ftth_ont AS o
   #    JOIN crm_cliente AS c
   #    ON o.serialnumber = c.serialnumber
   #    """
   # df_joined = pd.read_sql_query(queryjoin, con=connection)
   # print(df_joined)