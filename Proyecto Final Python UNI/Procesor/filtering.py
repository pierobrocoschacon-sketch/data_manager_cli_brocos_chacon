import pandas as pd
def lista_activos(df_prices):
    width = 45
    activos = df_prices.columns[1:].tolist()
    print("Los activos disponibles son:")
    for activo in activos:
        print(activo.center(width))
    return activos

def filtrar_activos(df_prices):
    width = 45
    activos_disponibles = lista_activos(df_prices)
    activos_seleccionados = []
    print("\nIngrese los tickers que desea conservar.")
    print("Escriba 'finalizar' para terminar")
    while True:
        entrada = input("Ingrese un ticker: ").strip()
        #Especificaremos un flujo con 4 posibles casos, el primero será "finalzar" que termina todo el
        #proceso de ingreso
        #El segundo es cuando ingreso un activo que ya estaba seleccionado
        #El tercero cuando ingreso un activo inválido
        if entrada.lower() == "finalizar":
            if len(activos_seleccionados) == 0:
                print("Usted no ha seleccionado ningún activo a filtrar".center(width))
                return df_prices, []
            else:
                break #finaliza el bucle dado que ya no se necesitan ingresar más tickers de filtrado
        if entrada not in activos_disponibles:
            print(f"{entrada} no es un activo válidos".center(width))
            continue
        if entrada in activos_seleccionados:
            print(f"{entrada} ya fue seleccionado antes".center(width))
            print("Activos seleccionados hasta ahora:")
            print(activos_seleccionados)
            print("Recuerde: Escribir 'finalizar' para terminar la selección")
            continue
        #Si no saltan cualquiera de esos casos, ahora recién agrego mi activo a mi filtering
        activos_seleccionados.append(entrada)

        print("Activo agregado correctamente".center(width))
        print("Activos seleccionados hasta ahora:")
        print(activos_seleccionados)
        print("Recuerde: Escribir 'finalizar' para terminar la selección")

        
    
    columnas_finales = [df_prices.columns[0]] + activos_seleccionados #concateno mi necesaria columna Dates más lo que yo quise filtrar
    df_filtrado = df_prices[columnas_finales]

    print("\n Filtrado completado".center(width))
    print("Activos finales seleccionados:")
    print(activos_seleccionados)

    return df_filtrado, activos_seleccionados

def filtrar_sector(df_prices,df_assets):
    width = 45
    sectores = df_assets["Sector"].unique().tolist()
    print("Sectores Disponibles:")
    for i,sector in enumerate(sectores, start = 1):
        print(f"{i}) {sector}")
    while True:
        try:
            opcion_sector = int(input("Seleccione el sector que desea filtrar: "))
            if (opcion_sector <= 0) or (opcion_sector > len(sectores)):
                print("Error, opción fuera de parámetros, seleccione una opción válida: ")
            else:
                sector_elegido = sectores[opcion_sector-1]
                tickers_sector = df_assets[df_assets["Sector"] == sector_elegido]["ticker"].tolist()
                columnas_disponibles = [col for col in tickers_sector if col in df_prices.columns]
                #En este caso se puede crear un bucle for dentro de una lista, esto para que el trabajo de filtrar
                #quienes son los tickers_sector que aparecen como pertenecientes a cierto sector en el df_assets y que
                #efectivamente también están en el df_prices
                columnas_finales = [df_prices.columns[0]] + columnas_disponibles
                #Le pongo corchetes a df_prices.columns ya que como "columnas_disponibles" es una lista
                #par que el operador "+" haga sentido se debe sumar lista con lista
                df_filtrado = df_prices[columnas_finales]
                print(f"Sector elegido: {sector_elegido}")
                print(df_filtrado)
                return df_filtrado
                break
        except ValueError:
            print("Error, por favor seleccione una opción válida")
            continue



    
def filtrar_paises(df_prices,df_assets):
    width = 45
    paises = df_assets["Pais"].unique().tolist()
    print("Países Disponibles:")
    for i,pais in enumerate(paises, start = 1):
        print(f"{i}) {pais}")
    while True:
        try:
            opcion_pais = int(input("Seleccione el país que desea filtrar: "))
            if (opcion_pais <= 0) or (opcion_pais > len(paises)):
                print("Error, opción fuera de parámetros, seleccione una opción válida: ")
            else:
                pais_elegido = paises[opcion_pais-1]
                tickers_pais = df_assets[df_assets["Pais"] == pais_elegido]["ticker"].tolist()
                columnas_disponibles = [col for col in tickers_pais if col in df_prices.columns]
                #En este caso se puede crear un bucle for dentro de una lista, esto para que el trabajo de filtrar
                #quienes son los tickers_sector que aparecen como pertenecientes a cierto sector en el df_assets y que
                #efectivamente también están en el df_prices
                columnas_finales = [df_prices.columns[0]] + columnas_disponibles
                #Le pongo corchetes a df_prices.columns ya que como "columnas_disponibles" es una lista
                #par que el operador "+" haga sentido se debe sumar lista con lista
                df_filtrado = df_prices[columnas_finales]
                print(f"Pais elegido: {pais_elegido}")
                print(df_filtrado)
                return df_filtrado
                break
        except ValueError:
            print("Error, por favor seleccione una opción válida")
            continue
    
