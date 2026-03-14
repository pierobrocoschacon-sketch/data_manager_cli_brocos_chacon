import os #Libreria base para manipular directorios dentro de la computadora
import sys #Libreria usada dentro de clase 
from Utils.menu_menues import lineador
import pandas as pd

def main():
    width = 45
    print("Ejecutando cargador".center(width))


def detectar_bases_datos():
    width = 45
    ruta_script = os.path.abspath(sys.argv[0]) #Donde se está ejecutando mi modulo, con especificamente my python
    #carpeta_script = os.path.dirname(ruta_script) #Ruta de la carpeta donde se está ejecutando mi modulo
    #(Linea superior comentada porque ahora se ejecutará desde Interfaz.py)
    proyecto_carpeta = os.path.dirname(ruta_script) #Que carpeta contiene el proyecto, que a su ves es donde están el resto
    #de carpetas que contienen distintos módulos
    #debiera de ser la carpeta que tiene la data, data loader, exporter, utils, etc
    ruta_data = os.path.join(proyecto_carpeta, "Data")
    #Guarda en una variable una ruta añadiendo /Data a la carpeta en donde vive el modulo de trabajo
    #aún no sé si eso existirá o no, de momento solo estoy hipotetizando sobre la existencia de una 
    #posible ruta
    if not os.path.exists(ruta_data):
        print("Error Crítico !!!".center(width))
        lineador()
        print("La carpeta del programa no contiene Carpeta Data".center(width))
    else:
        print("Todo ok :D".center(width))
        carpetas = os.listdir(ruta_data)

        bases_validas = []
        bases_invalidas = []

        for carpeta in carpetas:
            ruta_carpeta = os.path.join(ruta_data,carpeta) #me dedicaré a explorar carpeta por carpeta
            #para ver si tienen los necesarios para ser una base de datos "en condiciones" como el proyecto
            #especificaw
            if not os.path.isdir(ruta_carpeta): #verifico que la ruta sea en efecto una carpeta y que no haya
            #sido contaminada por cualquier archivo que dio erroneamente un nombre
                continue #si en caso no es una carpeta, y es una ruta ficticia contaminada por cualquier tonteria
                #simplemente ignooro esta iteración del bucle carpeta in carpetas y paso a la siguiente

            archivos = os.listdir(ruta_carpeta) #me valida que cosas hay dentro de la carpeta que estoy trabajando

            tiene_assets = False #en mi estructura de data, es indispensable que existe el archivo assetets.csv
            tiene_prices = False

            for archivo in archivos:
                if archivo == "assets.csv":
                    tiene_assets = True #Verifico que existe el indispensable assets.csv
                if archivo.startswith("prices_") and archivo.endswith(".csv"):
                    tiene_prices = True
            if (tiene_assets == 1 ) and (tiene_prices == 1):
                bases_validas.append(carpeta)
            else:
                bases_invalidas.append(carpeta)

            #Este último bucle me dice que basta con que una carpeta dentro de Data tiene el archivo assets.csv y
            #también el archivo que inicia con prices_ y acaba en .csv entonces en nuestro modelo ya es apto para
            #ser considerada una base de datos (lo de csv es realmente porque el proyecto va de leer archivos csv)
        return bases_validas, bases_invalidas
        print("Las bases válidas son:",bases_validas)
        print("Las bases inválidas son:",bases_invalidas)

def cargar_datos():
    ruta_script = os.path.abspath(sys.argv[0])
    #carpeta_script = os.path.dirname(ruta_script)
    proyecto_carpeta = os.path.dirname(ruta_script)
    ruta_data = os.path.join(proyecto_carpeta, "Data")

    bases_validas,_  = detectar_bases_datos()

    if not bases_validas: #aplicar un if a listas te devuelve True si estas tienen elementos dentro
        print("Ninguna base de datos válida")
        return None, None, None 
        #RECUERDA QUE DEBEMOS DE BUSCAR LA FORMA PARA QUE ESTO ME DEVUELVA AL MENU PRINCIPAL

    print("\nBases de datos válidas disponible:\n")
    for i, base in enumerate(bases_validas, start = 1):
        print(f"{i}. {base}") #Le asigno un número a cada una de las bases válidas para tener facilidadd de cargarlas

    while True:
        try:
            seleccion = int(input("\n Seleccione el número de la base a cargar: ").strip())
            if seleccion < 1 or seleccion > len(bases_validas): #Pongo este condicionar para facilitar el truncamiento de las
                #opciones disponibles dentro de la base de datos
                print("Error: seleccione un número válido.")
                continue
            base_elegida = bases_validas[seleccion-1] #-1 porque los indices de python empiezan desde cero
            ruta_base = os.path.join(ruta_data, base_elegida)
            archivos = os.listdir(ruta_base)

            ruta_assets = os.path.join(ruta_base, "assets.csv") #Esta ruta para assets es más direca, debido a que siempre
            #el archivo se llamará de la misma forma en todas las bases de datos
            ruta_prices = None #Esta no es tan directa porque siempre empieza con prices_ le sigue cualquier cosa y termina con .csv
            #creo que debí pensar mejor ese punto...

            for archivo in archivos:
                if archivo.startswith("prices_") and archivo.endswith(".csv"):
                    ruta_prices = os.path.join(ruta_base, archivo)
                    break #bucle que comprueba uno por uno si existe el archivo con precios

            #Lectura de la base de datos (usamos with statement como vimos en clase)
            #pandas permite hacerlo directamente, pero creo que deberiamos de ver lo que se usó en clase
            with open(ruta_assets, "r",encoding="utf-8-sig") as f_assets: #el encoding es debido a un tema de 
                #como es que se baja la data de bloomberg, sin eso la variable "Dates" sale rara en la lectura
                df_assets = pd.read_csv(f_assets)
            with open(ruta_prices, "r",encoding="utf-8-sig") as f_prices:
                df_prices = pd.read_csv(f_prices)
            print(f"Base '{base_elegida}' cargada correctamente.")
            print(f"Tamaño de Assets... Filas: {df_assets.shape[0]}, Columnas: {df_assets.shape[1]}")
            print(f"Tamaño de Precios... Filas: {df_prices.shape[0]}, Columnas: {df_prices.shape[1]}")

            return df_assets, df_prices, base_elegida #base elegida es solo el string que contiene
            #el nombre de la base de datos

        except ValueError:
            print("Error: debe ingresar un número entero.")
        except FileNotFoundError:
            print("Error: no se encontró uno de los archivos CSV requeridos (Prices o Assets)")
            return None, None, None

def visualizar(df_assets, df_prices, base_elegida):
    width = 45
    if df_assets is None or df_prices is None:
        print("No hay datos cargados para visualizar".center(width))
        return
    lineador()
    print(f"Base de datos cargada: {base_elegida}".center(width))
    lineador()

    print("\n--- INFORMACIÓN DE ASSETS ---")
    print(f"Filas: {df_assets.shape[0]}")
    print(f"Columnas: {df_assets.shape[1]}")
    print("\nColumnas:")
    print(list(df_assets.columns))

    print("\nPrimeras filas de assets:")
    print(df_assets.head())

    lineador()

    print("\n--- INFORMACIÓN DE PRECIOS ---")
    print(f"Filas: {df_prices.shape[0]}")
    print(f"Columnas: {df_prices.shape[1]}")
    print("\nColumnas:")
    print(list(df_prices.columns))

    print("\nPrimeras filas de precios:")
    print(df_prices.head())

    lineador()

if __name__ == "__main__":
    main()