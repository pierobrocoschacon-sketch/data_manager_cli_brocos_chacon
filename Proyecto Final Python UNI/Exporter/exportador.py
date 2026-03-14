import os
import json
import pandas as pd


def crear_carpeta_exportaciones():
    #Dentro de la estructura del proyecto no especifica un lugar especifico
    #donde guardar las exportaciones, sin embargo, sería una buena idea tenerlo
    #por temas de orden
    ruta_actual = os.getcwd()
    ruta_exportaciones = os.path.join(ruta_actual, "Exportaciones")

    if not os.path.exists(ruta_exportaciones):
        os.makedirs(ruta_exportaciones)

    return ruta_exportaciones


def preparar_df_para_json(df):
    df_export = df.copy()

    # Convertir NaN en None para que JSON lo maneje bien
    df_export = df_export.astype(object)
    df_export = df_export.where(pd.notna(df_export), None)

    return df_export


def exportar_base_json(df, nombre_archivo):
    ruta_exportaciones = crear_carpeta_exportaciones()
    df_export = preparar_df_para_json(df)

    contenido = {
        "columnas": df_export.columns.tolist(),
        "index": df_export.index.tolist(),
        "data": df_export.values.tolist()
    }

    ruta_final = os.path.join(ruta_exportaciones, f"{nombre_archivo}.json")

    with open(ruta_final, "w", encoding="utf-8") as archivo:
        #json.dump es como se escriben datos en un formato json
        json.dump(contenido, archivo, indent=4, ensure_ascii=False, default=str)

    return ruta_final


def exportar_estadisticos_json(df_stats, nombre_archivo):
    ruta_exportaciones = crear_carpeta_exportaciones()
    df_export = preparar_df_para_json(df_stats)

    contenido = {
        "columnas": df_export.columns.tolist(),
        "index": df_export.index.tolist(),
        "data": df_export.values.tolist()
    }

    ruta_final = os.path.join(ruta_exportaciones, f"{nombre_archivo}.json")

    with open(ruta_final, "w", encoding="utf-8") as archivo:
        json.dump(contenido, archivo, indent=4, ensure_ascii=False, default=str)

    return ruta_final