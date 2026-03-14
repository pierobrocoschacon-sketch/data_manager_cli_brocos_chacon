# data_manager_cli_brocos_chacon
Proyecto Final para el curso de la Pre Maestría de la UNI

Este proyecto está encargado de ejecutar directamente desde la consola un archivo .py teniendo una ruta bien establecida de directorio de trabajo
Lanzará un menú con diversas funciones, dentro de las cuales la principal es leer Data Financiera previamente descargada
El programa se lanza con el archivo interfaz.py

Lo que en este proyecto se considera "Data" es en realidad una carpeta con dos archivos .csv
1) assets.csv, que es una base de datos con todos los tickers de activos financieros, los nombres de sus compañías, el sector al que pertenecen y su país de origen
2) prices_xxxx.csv que es un archivo que tiene las series de tiempo de todos los tickers que se están manejando dentro del proyecto
Si dentro de la carpeta Data hay otra subcarpeta que contenga estos dos archivos .csv entonces se detecta que la carpeta cumple las condiciones
para ser tratada como una "base de datos" dentro del proyecto

Detalle importante, la data es real, y ha sido contaminada intencionalmente con valores negativos, ceros y nombres de idols coreanas femeninas

Posterior a ello, habrá distintas funciones que nos permitan limpiar la data para que esté lista para su lectura
filtrar la data según opciones disponibles, calcular estadísticos relevante y exportar los resultados que hemos calculado
internamente 

Además, también contamos con un modulo de testeo para pytest: testeo.py, el cual contiene diversos test de calidad de código

####################
\n 
Se han usado:
  Pandas: Dado que se trabaja con un dataframe de data de varias observaciones, es lo más eficiente
  para la gestión de la información del archivo

  OS: Debido a la estructura del proyecto organizado carpeta por carpeta y dado que no se ha tocado
  el uso de archivos "__file__"
\n
####################

$$$$$$$$$$$$$$$$$$EJEMPLO DOCUMENTADO DE EJECUCIÓN $$$$$$$$$$$$$$$$$$$$$$$$


:)
