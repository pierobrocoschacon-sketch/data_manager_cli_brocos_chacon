import pandas as pd
import pandas as pd

def df_ret(df_prices):

    df = df_prices.copy()
    df = df.sort_values("Dates").reset_index(drop=True)
    fechas = df[["Dates"]]
    precios = df.drop(columns=["Dates"])
    precios = precios.ffill() #Sin esto no voy a poder generar retornos consistentes
    #porque mi base de datos puede tener NaNs, conforme a como se cotizan los precios
    #en bloomberg si no tenemos valor para un día lo podemos reemplazar con su último
    #valor de cierre registrado
    rets = precios / precios.shift(1) - 1
    df_rets = pd.concat([fechas, rets], axis=1)

    return df_rets

def cal_prom(df_prices):
    df = df_prices.copy()
    activos = df.iloc[:, 1:].copy()
    
    promedios = activos.mean().to_frame().T
    promedios.index = ["Promedio"]
    
    return promedios


def cal_stdevs(df_prices):
    df = df_prices.copy()
    activos = df.iloc[:, 1:].copy()
    
    stdevs = activos.std().to_frame().T
    stdevs.index = ["Stdev"]
    
    return stdevs


def cal_sesgo(df_prices):
    df = df_prices.copy()
    activos = df.iloc[:, 1:].copy()
    
    sesgos = activos.skew().to_frame().T
    sesgos.index = ["Sesgo"]
    
    return sesgos


def cal_kurtosis(df_prices):
    df = df_prices.copy()
    activos = df.iloc[:, 1:].copy()
    
    kurtosis = activos.kurt().to_frame().T
    kurtosis.index = ["Kurtosis"]
    
    return kurtosis


def cal_max_val(df_prices):
    df = df_prices.iloc[:,1:].copy()
    maximos = df.max().to_frame().T
    maximos.index = ["Max_Valor"]
    return maximos


def cal_max_fecha(df_prices):

    fechas = {}
    activos = df_prices.columns[1:]

    for col in activos:
        fila_max = df_prices[col].idxmax()
        fechas[col] = df_prices.loc[fila_max, "Dates"]

    df_fechas_max = pd.DataFrame([fechas])
    df_fechas_max.index = ["Max_Fecha"]

    return df_fechas_max

def cal_min_val(df_prices):
    df = df_prices.iloc[:,1:].copy()
    minimos = df.min().to_frame().T
    minimos.index = ["Min_Valor"]
    return minimos


def cal_min_fecha(df_prices):

    fechas = {}
    activos = df_prices.columns[1:]

    for col in activos:
        fila_min = df_prices[col].idxmin()
        fechas[col] = df_prices.loc[fila_min, "Dates"]

    df_fechas_min = pd.DataFrame([fechas])
    df_fechas_min.index = ["Min_Fecha"]

    return df_fechas_min


def cal_estadisticos(df_prices, df_assets):

    tickers = df_prices.columns[1:]

    nombres = {}
    for t in tickers:
        nombre = df_assets.loc[df_assets["ticker"] == t, "Nombre"].values
        nombres[t] = nombre[0]


    df_nombres = pd.DataFrame([nombres])
    df_nombres.index = ["Nombre"]

    prom = cal_prom(df_prices)
    stdev = cal_stdevs(df_prices)
    sesgo = cal_sesgo(df_prices)
    kurt = cal_kurtosis(df_prices)

    max_val = cal_max_val(df_prices)
    max_fecha = cal_max_fecha(df_prices)

    min_val = cal_min_val(df_prices)
    min_fecha = cal_min_fecha(df_prices)

    df_stats = pd.concat(
        [
            df_nombres,
            prom,
            stdev,
            sesgo,
            kurt,
            max_val,
            max_fecha,
            min_val,
            min_fecha
        ],
        axis=0
    )

    return df_stats
    