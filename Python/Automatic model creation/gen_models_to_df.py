import subprocess
import importlib
import os
import sys
import pandas as pd
from django.apps import apps


MODELS_PATH = 'consolidacion.models_generated'
MODELS_FILEPATH = MODELS_PATH.replace('.', '/') + '.py' 


#Con inspect db regenera el archivo models_generated.py
def upload_models_db():
    """Regenera el archivo de modelos desde la BD, limpia 2 primeras líneasy borra el archivo previamente si existe"""
    if os.path.exists(MODELS_FILEPATH):
        os.remove(MODELS_FILEPATH)
        print(f"{MODELS_FILEPATH} eliminado previamente.")

    subprocess.run(
        "python manage.py inspectdb > " + MODELS_FILEPATH,
        shell=True, # se ejecutará en la shell
        check=True # me avisará si el comando falla
    )
    clean_file(MODELS_FILEPATH)
    print("Modelos actualizados")

#Limpia 2 primeras lineas generadas por Django
def clean_file(filepath: str):
    """Limpia el archivo generado por inspectdb, eliminando las 2 primeras líneas"""
    with open(filepath, 'r') as fr:
        # Lee todas las líneas del archivo
        lines = fr.readlines()

    with open(filepath, "w") as fw:
        ## sobreescribe sin las primeras (se puede hacer en un nuevo archivo para no borrar el originalque devuelve inspectdb)
        fw.writelines(lines[2:])


def retrieve_models(selected_models: list):
    """Recarga el módulo de modelos y devuelve el modelo dinámicamente"""
 # Limpia manualmente el registro de modelos para la app "consolidacion" #Tratar de evitar esta recarga dinámica!! RIESGO
    app_config = apps.get_app_config('consolidacion') #obtiene config de la app
    app_config.models.clear()# borra diccionario de modelos SI SE HACE ESTO DESPUES DE CARGAR MODELOS Y CREADO TABLAS; PUEDE CAUSAR FALLOS 
    apps.all_models['consolidacion'].clear() # Limpia caché de consolidacion

    # Recarga el módulo de modelos
    if MODELS_PATH in sys.modules:
        del sys.modules[MODELS_PATH] #Elimina el modulo si ya está cargado
    module = importlib.import_module(MODELS_PATH) #Vuelve a cargar el módulo
    retrieved_models = {}
    for model in selected_models: #Itera sobre los módulos para sacar los elegidos
        try:
            retrieved_models[model] = getattr(module, model)  # Obtiene el modelo dinámicamente
        except AttributeError:
            print(f"Modelo '{model}' no encontrado.")
    
    return retrieved_models




def generate_dataframe(selected_models: list):
    """Actualiza modelos, recarga ORM y devuelve DataFrames para los modelos selccionados"""
    upload_models_db() 
    models_retrieved = retrieve_models(selected_models) #Recupera el modulo elegido
    dataframes = {}

    for model_name, model in models_retrieved.items():
        queryset = model.objects.all().values()
        df = pd.DataFrame(list(queryset))
        dataframes[model_name] = df
       # print(f"DataFrame para el modelo {model_name} actualizado:")
       # print(df.head())
       # print("------------------------------------------------")

    return dataframes


#Probando salir de la sesión 
def get_dataframe_and_restart(selected_models: list):
    generate_dataframe(selected_models)
    os.execvp(sys.executable, [sys.executable] + sys.argv)
