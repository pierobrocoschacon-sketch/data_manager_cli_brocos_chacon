import pandas as pd
import numpy as np


def limpieza(base_prices):
    width = 45
    print("Limpiando base de datos...".center(width))
    #Por seguridad, copio el df para no modificar el original por error
    df_limpio = base_prices.copy()
    col_fechas = df_limpio.columns[0]
    tickers = list(df_limpio.columns[1:])
    
    total_aberraciones = 0
    detalle_aberraciones = {}

    for ticker in tickers:
        aberraciones_ticker = 0
        for idx in df_limpio.index:
            valor_original = df_limpio.loc[idx,ticker]
            if pd.isna(valor_original):
                continue
            valor_numerico = pd.to_numeric(pd.Series([valor_original]),errors = "coerce").iloc[0] #trato de convertir un string a valor numerico
            #si fallo, porque el string es algo como "Jennie" entonces ya lo relleno de una vez con un NaN
            #se hace el "truco" se tener que convertir una sola celda a una serie de pandas
            #debido a que pd.to_numeric es util en este aspecto y funciona con objetos pandas
            #lógicamente como es una serie de un elemento .iloc[0] devuelve el único elemento que hay

            if pd.isna(valor_numerico):
                df_limpio.loc[idx,ticker] = np.nan
                aberraciones_ticker =  aberraciones_ticker+1
                continue

            if valor_numerico <= 0:
                df_limpio.loc[idx,ticker] = np.nan
                aberraciones_ticker =  aberraciones_ticker+1
                continue
            #Si no tiene ninguna aberración, lo dejamos así nomas
            df_limpio.loc[idx,ticker] = float(valor_numerico)
        detalle_aberraciones[ticker] = aberraciones_ticker #cuanto cuantas aberraciones por ticker encontré 
        total_aberraciones = total_aberraciones+aberraciones_ticker
    print(f"Total de aberraciones corregidas: {total_aberraciones}".center(width))
    print("\nDetalle de aberraciones por ticker:")
    for ticker,cantidad in detalle_aberraciones.items():
        print(f"El ticker {ticker} tuvo: {cantidad} aberraciones")
    return df_limpio