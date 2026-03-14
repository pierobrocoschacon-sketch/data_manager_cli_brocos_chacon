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

$$$$$$$$$$$$$$$$$$ EJEMPLO DOCUMENTADO DE EJECUCIÓN $$$$$$$$$$$$$$$$$$$$$$$$

## Ejemplo documentado de ejecución

El programa se ejecuta desde la carpeta raíz del proyecto con el siguiente comando:

```bash
py interfaz.py
```

Al iniciar, el sistema muestra el menú principal del Explorador de Activos Financieros:

```text
PS C:\Users\Piero\Downloads\Proyecto Final Python UNI> py interfaz.py
=============================================
      Explorador de Activos Financieros
                  Bienvenido
         Por favor, elija una opción
=============================================
                1) Cargar data
               2) Validar datos
               3) Filtrar datos
               4) Ordenar datos
           5) Mostrar estadísticas
            6) Exportar resultados
                   7) Salir
=============================================
```

### 1. Carga de una base de datos

El usuario selecciona la opción 1 para cargar una base de datos disponible:

```text
           Seleccione una opción:            1
            Opción 1 seleccionada
                  Todo ok :D
     La cantidad de bases válidas son: 2
=============================================
Por favor, seleccione un base de datos disponible:
                  Todo ok :D

Bases de datos válidas disponible:

1. No tocar
2. set 2 (corrupto)
```

Luego, el usuario selecciona la base `set 2 (corrupto)`:

```text
 Seleccione el número de la base a cargar: 2
Base 'set 2 (corrupto)' cargada correctamente.
Tamaño de Assets... Filas: 24, Columnas: 4
Tamaño de Precios... Filas: 9568, Columnas: 25
=============================================
   Base de datos cargada: set 2 (corrupto)
=============================================
```

A continuación, el programa muestra un resumen de la base cargada. Para `assets.csv`, se observa la estructura de metadatos de los activos:

```text
--- INFORMACIÓN DE ASSETS ---
Filas: 24
Columnas: 4

Columnas:
['ticker', 'Nombre', 'Sector', 'Pais']

Primeras filas de assets:
  ticker                  Nombre      Sector     Pais
0   AAPL              Apple Inc.  Technology      USA
1   MSFT   Microsoft Corporation  Technology      USA
2   6758  Sony Group Corporation  Technology    Japan
3   9984    SoftBank Group Corp.  Technology    Japan
4    SAP                  SAP SE  Technology  Germany
=============================================
```

También se presenta la información general del archivo de precios:

```text
--- INFORMACIÓN DE PRECIOS ---
Filas: 9568
Columnas: 25

Columnas:
['Dates', 'AAPL', 'MSFT', '6758', '9984', 'SAP', 'TOTS3', 'JPM', '8306', '8411', 'DBK', 'CBK', 'BBDC4', 'XOM', 'CVX', '1605', 'EOAN', 'PETR4', 'PRIO3', 'KO', 'MCD', '2502', 'ADS', 'ABEV3', 'LREN3']
```

### 2. Validación y limpieza de datos

Luego, el usuario selecciona la opción 2 para validar la data cargada:

```text
                1) Cargar data
               2) Validar datos
               3) Filtrar datos
               4) Ordenar datos
           5) Mostrar estadísticas
            6) Exportar resultados
                   7) Salir
=============================================
           Seleccione una opción:            2
            Opción 2 seleccionada
         Examinando data cargada....
=============================================
La base de datos cargada es: set 2 (corrupto)
=============================================
```

El sistema muestra la base de precios y luego pregunta si se desea limpiar la información:

```text
Desea limpiar la data ? Seleccione una opción
1) Sí
2) No
Eliga una opción:1
          Limpiando base de datos...
    Total de aberraciones corregidas: 9184
```

Además, el programa detalla cuántas aberraciones fueron corregidas por ticker. Por ejemplo:

```text
Detalle de aberraciones por ticker:
El ticker AAPL tuvo: 385 aberraciones
El ticker MSFT tuvo: 392 aberraciones
El ticker 6758 tuvo: 416 aberraciones
...
El ticker LREN3 tuvo: 370 aberraciones
```

Esto demuestra que la aplicación detecta y corrige valores inválidos dentro de la base de precios, como textos en lugar de números, precios negativos y otros registros inconsistentes.

### 3. Ordenamiento de la base de datos

Después de limpiar la data, el usuario puede ordenar la base por fecha. En este caso, selecciona la opción 4 del menú principal y luego el criterio “Más antiguo a más reciente”:

```text
                1) Cargar data
               2) Validar datos
               3) Filtrar datos
               4) Ordenar datos
           5) Mostrar estadísticas
            6) Exportar resultados
                   7) Salir
=============================================
           Seleccione una opción:            4
            Opción 4 seleccionada
            Seleccione una opción
=============================================
        1) Más antiguo a más reciente
        2) Más reciente a más antiguo
                  3) Volver
=============================================
       Seleccione un criterio de orden       1
```

El resultado es una tabla de precios ordenada cronológicamente, comenzando en `1999-12-31` y terminando en `2026-03-11`.

### 4. Filtrado por activos específicos

El usuario también puede filtrar por tickers concretos. Para ello, entra a la opción 3 y elige “Filtrado por Securities”:

```text
                1) Cargar data
               2) Validar datos
               3) Filtrar datos
               4) Ordenar datos
           5) Mostrar estadísticas
            6) Exportar resultados
                   7) Salir
=============================================
           Seleccione una opción:            3
            Opción 3 seleccionada
      Seleccione un criterio de filtrado
=============================================
          1) Filtrado por Securities
           2) Filtado por Sectores
            3) Filtrado por Países
         4) Volver al menú principal
=============================================
Seleccione una opción1
```

El programa lista todos los activos disponibles y permite al usuario ir agregando tickers manualmente. En este ejemplo, el usuario elige `AAPL`, `MSFT`, `JPM`, `2502`, `8411` y `8306`, finalizando con la palabra `FINALIZAR`:

```text
Ingrese un ticker: AAPL
        Activo agregado correctamente
Activos seleccionados hasta ahora:
['AAPL']

Ingrese un ticker: MSFT
        Activo agregado correctamente
Activos seleccionados hasta ahora:
['AAPL', 'MSFT']

Ingrese un ticker: JPM
        Activo agregado correctamente
Activos seleccionados hasta ahora:
['AAPL', 'MSFT', 'JPM']

Ingrese un ticker: 2502
        Activo agregado correctamente
Activos seleccionados hasta ahora:
['AAPL', 'MSFT', 'JPM', '2502']

Ingrese un ticker: 8411
        Activo agregado correctamente
Activos seleccionados hasta ahora:
['AAPL', 'MSFT', 'JPM', '2502', '8411']

Ingrese un ticker: 8306
        Activo agregado correctamente
Activos seleccionados hasta ahora:
['AAPL', 'MSFT', 'JPM', '2502', '8411', '8306']

Ingrese un ticker: FINALIZAR

 Filtrado completado
Activos finales seleccionados:
['AAPL', 'MSFT', 'JPM', '2502', '8411', '8306']
```

### 5. Filtrado por sector

Otra opción disponible es el filtrado por sector. En este caso, el usuario selecciona el sector `Technology`:

```text
Seleccione una opción2
Filtrando por Sector...
Sectores Disponibles:
1) Technology
2) Financials
3) Energy
4) Consumer
Seleccione el sector que desea filtrar: 1
Sector elegido: Technology
```

El programa devuelve una base con la columna de fechas y los activos correspondientes a ese sector. En la ejecución mostrada, el resultado contiene las series de `AAPL` y `MSFT`.

### 6. Cálculo de estadísticas

Finalmente, el usuario selecciona la opción 5 para calcular estadísticas descriptivas sobre la base filtrada:

```text
                1) Cargar data
               2) Validar datos
               3) Filtrar datos
               4) Ordenar datos
           5) Mostrar estadísticas
            6) Exportar resultados
                   7) Salir
=============================================
           Seleccione una opción:            5
            Opción 5 seleccionada
=============================================
Calculando estadísticos
                          AAPL                   MSFT
Nombre              Apple Inc.  Microsoft Corporation
Promedio             51.484664             108.567862
Stdev                71.810454             131.205983
Sesgo                 1.515253               1.596397
Kurtosis               1.02854               1.303173
Max_Valor               286.19                 542.07
Max_Fecha  2025-12-02 00:00:00    2025-10-28 00:00:00
Min_Valor               0.2346                  15.15
Min_Fecha  2003-04-21 00:00:00    2009-03-09 00:00:00
=============================================
```

Luego, el sistema pregunta si se desean calcular estadísticas sobre los retornos:

```text
Desea calcular los estadísticos de los retornos ?
1) Sí
2) No
Seleccione una opción: 1
```

El programa genera primero la serie de retornos y después muestra los estadísticos correspondientes:

```text
                          AAPL                   MSFT
Nombre              Apple Inc.  Microsoft Corporation
Promedio              0.000797               0.000324
Stdev                 0.019941               0.015602
Sesgo                -1.639508               0.173493
Kurtosis              56.73012              16.369403
Max_Valor             0.201324               0.195652
Max_Fecha  2004-10-18 00:00:00    2000-10-19 00:00:00
Min_Valor            -0.518736              -0.155979
Min_Fecha  2000-09-29 00:00:00    2000-04-24 00:00:00
=============================================
```

### 7. Salida del programa y ejecución de tests

Una vez concluido el flujo principal, el usuario selecciona la opción 7 para salir del sistema:

```text
=============================================
           Seleccione una opción:            7
            Opción 7 seleccionada
            Nos vemos pronto ! :)
           Finalizando programa...
=============================================
```

Posteriormente, se ejecutan los tests automatizados del proyecto con `pytest`:

```text
PS C:\Users\Piero\Downloads\Proyecto Final Python UNI> pytest testeo.py
==================================================================================================== test session starts ====================================================================================================
platform win32 -- Python 3.13.1, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\Piero\Downloads\Proyecto Final Python UNI
collected 7 items

testeo.py .......                                                                                                                                                                                                      [100%]

===================================================================================================== 7 passed in 0.38s =====================================================================================================
PS C:\Users\Piero\Downloads\Proyecto Final Python UNI>
```

## Conclusión del ejemplo de ejecución

En esta ejecución documentada se observa el flujo principal del programa:

1. Se inicia el sistema desde terminal.
2. Se carga una base de datos válida desde la carpeta `Data`.
3. Se inspecciona la estructura de los archivos `assets.csv` y `prices_xxx.csv`.
4. Se valida y limpia la base de precios.
5. Se ordena la información por fecha.
6. Se realizan filtros por tickers y por sector.
7. Se calculan estadísticas tanto para precios como para retornos.
8. Se cierra correctamente el programa.
9. Se ejecutan los tests automatizados, los cuales pasan satisfactoriamente.

Este flujo demuestra que la aplicación cumple con las funcionalidades principales del proyecto CLI: carga de datos, validación, limpieza, filtrado, ordenamiento, análisis estadístico y testing del código.

Gracias por su tiempo !
