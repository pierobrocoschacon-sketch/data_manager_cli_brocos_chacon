import pandas as pd
import numpy as np
import pytest

from Procesor.estadisticos import df_ret
from Procesor.estadisticos import cal_prom
from Procesor.estadisticos import cal_stdevs
from Procesor.estadisticos import cal_max_fecha
from Procesor.estadisticos import cal_min_fecha
from Procesor.estadisticos import cal_estadisticos
from Utils.validador import limpieza

# Corre con:
# py -m pytest Testing/testeo.py

# Dado que las funciones matemáticas (mean, std, etc) se hacen con pandas
# es medio complicado buscarles un testeo creativo

def test_df_ret_calcula_retornos_y_respeta_dates():
    # Este test verifica dos cosas importantes:
    # 1) que la función ordene bien las fechas aunque entren desordenadas
    # 2) que calcule correctamente los retornos porcentuales
    # Es clave testear esto porque el cálculo de retornos depende totalmente
    # del orden temporal, si las fechas quedan mal, todo el análisis se malogra.

    df_prices = pd.DataFrame({
        "Dates": ["2024-01-03", "2024-01-01", "2024-01-02"],
        "AAPL": [121, 100, 110],
        "MSFT": [242, 200, 220]
    })

    resultado = df_ret(df_prices)

    assert resultado.columns.tolist() == ["Dates", "AAPL", "MSFT"]
    assert resultado.iloc[0]["Dates"] == "2024-01-01"
    assert resultado.iloc[1]["Dates"] == "2024-01-02"
    assert resultado.iloc[2]["Dates"] == "2024-01-03"

    assert pd.isna(resultado.iloc[0]["AAPL"])
    assert round(resultado.iloc[1]["AAPL"], 4) == 0.10
    assert round(resultado.iloc[2]["AAPL"], 4) == 0.10

    assert pd.isna(resultado.iloc[0]["MSFT"])
    assert round(resultado.iloc[1]["MSFT"], 4) == 0.10
    assert round(resultado.iloc[2]["MSFT"], 4) == 0.10


def test_cal_prom_devuelve_promedios_correctos():
    # Este test revisa que la función de promedios saque bien la media de cada activo
    # usando una base de precios limpia y coherente.


    df_prices = pd.DataFrame({
        "Dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "AAPL": [100, 110, 120],
        "MSFT": [200, 220, 240]
    })

    resultado = cal_prom(df_prices)

    assert resultado.index.tolist() == ["Promedio"]
    assert resultado.columns.tolist() == ["AAPL", "MSFT"]
    assert resultado.loc["Promedio", "AAPL"] == 110
    assert resultado.loc["Promedio", "MSFT"] == 220


def test_cal_stdevs_devuelve_desviaciones_correctas():
    # Este test comprueba que la desviación estándar de cada activo se calcule bien.
    # Es relevante porque la dispersión de precios es una medida básica de volatilidad,
    # entonces si esto sale mal, las estadísticas de riesgo también salen mal.

    df_prices = pd.DataFrame({
        "Dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "AAPL": [100, 110, 120],
        "MSFT": [200, 220, 240]
    })

    resultado = cal_stdevs(df_prices)

    assert resultado.index.tolist() == ["Stdev"]
    assert resultado.columns.tolist() == ["AAPL", "MSFT"]
    assert round(resultado.loc["Stdev", "AAPL"], 4) == 10.0000
    assert round(resultado.loc["Stdev", "MSFT"], 4) == 20.0000


def test_cal_max_fecha_devuelve_fecha_correcta():
    # Este test verifica que la función identifique correctamente
    # la fecha en la que cada activo alcanza su precio máximo.

    df_prices = pd.DataFrame({
        "Dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "AAPL": [100, 130, 120],
        "MSFT": [210, 205, 250]
    })

    resultado = cal_max_fecha(df_prices)

    assert resultado.index.tolist() == ["Max_Fecha"]
    assert resultado.loc["Max_Fecha", "AAPL"] == "2024-01-02"
    assert resultado.loc["Max_Fecha", "MSFT"] == "2024-01-03"


def test_cal_min_fecha_devuelve_fecha_correcta():
    # Este test revisa que la función encuentre bien
    # la fecha del precio mínimo para cada activo.


    df_prices = pd.DataFrame({
        "Dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "AAPL": [100, 130, 120],
        "MSFT": [210, 205, 250]
    })

    resultado = cal_min_fecha(df_prices)

    assert resultado.index.tolist() == ["Min_Fecha"]
    assert resultado.loc["Min_Fecha", "AAPL"] == "2024-01-01"
    assert resultado.loc["Min_Fecha", "MSFT"] == "2024-01-02"


def test_limpieza_reemplaza_strings_y_no_positivos_por_nan():
    # Acá sí tiene sentido meter data podrida, porque precisamente esta función
    # existe para limpiar precios inválidos.
    # Este test comprueba que textos, ceros y negativos sean convertidos a NaN,
    # mientras que los valores válidos sí se conserven.

    df_prices = pd.DataFrame({
        "Dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "AAPL": [100, "Jennie", -5],
        "MSFT": [200, 0, 220]
    })

    resultado = limpieza(df_prices)

    assert resultado.loc[0, "AAPL"] == 100.0
    assert pd.isna(resultado.loc[1, "AAPL"])
    assert pd.isna(resultado.loc[2, "AAPL"])

    assert resultado.loc[0, "MSFT"] == 200.0
    assert pd.isna(resultado.loc[1, "MSFT"])
    assert resultado.loc[2, "MSFT"] == 220.0


def test_cal_estadisticos_integra_todo_correctamente():
    # Al final el usuario no verá funciones sueltas, verá
    # una tabla resumen y esa tabla debe salir bien armada.

    df_prices = pd.DataFrame({
        "Dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "AAPL": [100, 110, 120],
        "MSFT": [200, 220, 210]
    })

    df_assets = pd.DataFrame({
        "ticker": ["AAPL", "MSFT"],
        "Nombre": ["Apple Inc.", "Microsoft Corp."]
    })

    resultado = cal_estadisticos(df_prices, df_assets)

    assert "AAPL" in resultado.columns
    assert "MSFT" in resultado.columns

    assert "Nombre" in resultado.index
    assert "Promedio" in resultado.index
    assert "Stdev" in resultado.index
    assert "Max_Valor" in resultado.index
    assert "Max_Fecha" in resultado.index
    assert "Min_Valor" in resultado.index
    assert "Min_Fecha" in resultado.index

    assert resultado.loc["Nombre", "AAPL"] == "Apple Inc."
    assert resultado.loc["Nombre", "MSFT"] == "Microsoft Corp."

    assert resultado.loc["Promedio", "AAPL"] == 110
    assert round(resultado.loc["Promedio", "MSFT"], 4) == 210.0000

    assert resultado.loc["Max_Valor", "AAPL"] == 120
    assert resultado.loc["Max_Fecha", "AAPL"] == "2024-01-03"

    assert resultado.loc["Min_Valor", "MSFT"] == 200
    assert resultado.loc["Min_Fecha", "MSFT"] == "2024-01-01"