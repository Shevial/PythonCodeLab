from django.db import models
import pandas as pd
from django.db import connection

class MySQLData:
    def __init__(self):
        pass
    
    def query_to_dataframe(self, sql_query):
        """Ejecutar una consulta SQL y devolver los resultados como un DataFrame de pandas"""
        with connection.cursor() as cursor:
            cursor.execute(sql_query)  # Ejecuto consulta SQL
            columns = [col[0] for col in cursor.description]  # Obtengo nombres de columnas de consulta
            results = cursor.fetchall()  # Obtengo todos los resultados de consulta
            df = pd.DataFrame(results, columns=columns)  # Creo DataFrame a partir de los resultados
        return df

def ejecutar_consulta():

    db = MySQLData()
    sql_query ="SELECT * FROM ftth_ont"
    df = db.query_to_dataframe(sql_query)
    print(df)
    return df


#WORKING 