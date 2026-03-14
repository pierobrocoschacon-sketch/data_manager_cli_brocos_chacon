from Utils.menu_menues import bienvenida
from Utils.menu_menues import mostrar_menu
from Utils.menu_menues import lineador
from Data_Loader.cargador_data import detectar_bases_datos
from Data_Loader.cargador_data import cargar_datos
from Data_Loader.cargador_data import visualizar
from Utils.validador import limpieza
from Procesor.filtering import lista_activos
from Procesor.filtering import filtrar_activos
from Procesor.filtering import filtrar_sector
from Procesor.filtering import filtrar_paises
from Procesor.estadisticos import cal_estadisticos
from Procesor.estadisticos import df_ret
from Exporter.exportador import exportar_base_json
from Exporter.exportador import exportar_estadisticos_json
from Utils.eliminador import eliminador

#ARREGLAR BOTON DE SALIDA DE LA PANTALLA DE CARGAR DATA
#ARREGLAR QUE PASA SI MI DF SE QUEDA CON PURAS COLUMNA FECHAS
def main():
    bienvenida()
    width = 45 #Si no lo creo de una vez va a ser un problema andar llamandolo desde otras funciones
    retornos_creados = 0
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opción: ".center(width)).strip())
            #Pongo strip() para no hacerme bolas con que haya diferencias entre "1" y "1    "
            #Pongo int() para evitarme poner integers en cada validador de condición, y de paso para usar
            #lo visto en clase de manejo de excepciones
            print(f"Opción {opcion} seleccionada".center(width))
            if opcion == 1:
                bases_validas, bases_invalidas = detectar_bases_datos()
                print(f"La cantidad de bases válidas son: {len(bases_validas)}".center(width))
                lineador()
                print("Por favor, seleccione un base de datos disponible:".center(width))
                df_assets, df_prices, base_elegida = cargar_datos()
                visualizar(df_assets, df_prices, base_elegida)
                data_limpia = 0

                #Si cargo una base nueva, todo lo previamente calculado deja de tener sentido
                #porque pertenecía a una base anterior
                retornos_creados = 0

                #Reseteo estas variables para evitar que se arrastre data vieja en memoria
                #y luego termine exportando o imprimiendo cosas incorrectas
                eliminador()

            elif opcion == 2:
                print("Examinando data cargada....".center(width))
                lineador()
                try:
                    print(f"La base de datos cargada es: {base_elegida}")
                    lineador()
                    print(df_prices)
                    lineador()
                    while True:
                        print("Desea limpiar la data ? Seleccione una opción".center(width))
                        print("1) Sí")
                        print("2) No")
                        try:
                            opcion_validar = int(input("Eliga una opción:"))
                            if opcion_validar == 1:
                                df_prices = limpieza(df_prices)
                                print(df_prices)
                                data_limpia = 1

                                #Si limpio nuevamente la base, cualquier retorno previo deja de ser válido
                                #porque ahora cambió el insumo base sobre el cual se calculaba todo
                                retornos_creados = 0
                                eliminador()

                                break
                            if opcion_validar == 2:
                                lineador()
                                print("Ok, data sin limpiar (posibles aberraciones en la data)")
                                lineador()
                                break
                            else:
                                print("Error, eliga una opción válida")
                                continue
                        except ValueError:
                            print("Error, eliga una opción válida")
                            continue
                        
                except NameError:
                    print("Error, no hay data cargada en la memoria".center(width))
                    print("Por favor, cargue data y repita el procedimiento".center(width))
                    lineador()
                    continue

            elif opcion == 3:
                print("Seleccione un criterio de filtrado".center(width))
                lineador()
                print("1) Filtrado por Securities".center(width))
                print("2) Filtado por Sectores".center(width))
                print("3) Filtrado por Países".center(width))
                print("4) Volver al menú principal".center(width))
                lineador()
                while True:
                    try:
                        opcion_filtrador = int(input("Seleccione una opción"))
                        try :
                            df_prices = df_prices
                            if opcion_filtrador ==1:
                                lista_activo = lista_activos(df_prices)
                                lineador()
                                df_prices, activos_seleccionados = filtrar_activos(df_prices)

                                #Filtrar cambia la base trabajada, así que los retornos viejos ya no sirven
                                retornos_creados = 0
                                eliminador()
                                break
                            elif opcion_filtrador ==2:
                                print("Filtrando por Sector...")
                                df_prices = filtrar_sector(df_prices,df_assets)

                                #Misma lógica, al cambiar la base también mueren derivados viejos
                                retornos_creados = 0
                                eliminador()

                                break
                            elif opcion_filtrador ==3:
                                print("Filtrando por País...")
                                df_prices = filtrar_paises(df_prices,df_assets)

                                #Misma lógica, al cambiar la base también mueren derivados viejos
                                retornos_creados = 0
                                eliminador()

                                break
                            elif opcion_filtrador == 4:
                                print("Volviendo al menú principal...")
                                break
                            else:
                                print("Por favor seleccione una opción válida")
                                continue
                        except NameError:
                            print("Volviendo al menú principal (no hay data)".center(width))
                            break
                    except ValueError:
                        print("Por favor seleccione una opción válida".center(width))
                        continue

            elif opcion == 4:
                try:
                    print("Seleccione una opción".center(width))
                    lineador()
                    print("1) Más antiguo a más reciente".center(width))
                    print("2) Más reciente a más antiguo".center(width))
                    print("3) Volver".center(width))
                    lineador()
                    while True:
                        try: 
                            opcion_sort = int(input("Seleccione un criterio de orden".center(width)))
                            if opcion_sort == 1:
                                df_prices = df_prices.sort_values(by="Dates").reset_index(drop=True)
                                #Poner reset_index evita futuros inconvenientes cuando se usa métodos como iloc o loc
                                print(df_prices)

                                #Al reordenar no cambias los valores, pero sí conviene invalidar derivados previos
                                #para mantener consistencia operativa del flujo
                                retornos_creados = 0
                                eliminador()

                                break
                            elif opcion_sort == 2:
                                df_prices = df_prices.sort_values(by="Dates",ascending = False).reset_index(drop=True)
                                print(df_prices)

                                #Misma lógica que arriba
                                retornos_creados = 0
                                eliminador()

                                break
                            elif opcion_sort == 3:
                                lineador()
                                print("Volviendo al menú principal...")
                                break
                            else:
                                print("Por favor, seleccione una opción válida".center(width))
                                continue
                        except ValueError:
                            print("Error, seleccione una opción correcta".center(width))
                except NameError:
                    print("No hay una base de datos cargada...".center(width))
            elif opcion == 5:
                try :
                    df_prices=df_prices
                    lineador()
                    if data_limpia == 0:
                        print("Primero debe limpiar la data (Disponible en Validar Data)")
                        continue
                    else:
                        print("Calculando estadísticos")
                        estadisticos = cal_estadisticos(df_prices,df_assets)
                        print(estadisticos)
                    lineador()
                    print("Desea calcular los estadísticos de los retornos ?".center(width))
                    print("1) Sí")
                    print("2) No")
                    while True:
                        try:
                            opcion_retornos = int(input("Seleccione una opción: "))
                            if opcion_retornos != 1 and opcion_retornos != 2:
                                print("Por favor, elija una opción válida")
                                continue
                            else:
                                if opcion_retornos ==2:
                                    break
                                elif opcion_retornos == 1:
                                    df_rets = df_ret(df_prices)
                                    print(df_rets)
                                    estadisticos_rets = cal_estadisticos(df_rets,df_assets)
                                    print(estadisticos_rets)
                                    retornos_creados = 1
                                    break
                        except ValueError:
                            print("Por favor, elija una opción válida")
                            continue
                except NameError:
                    lineador()
                    print("No hay una base de datos cargada".center(width))
                    lineador()
                    continue
                lineador()
            elif opcion == 6:
                try:
                    df_prices = df_prices
                    print("Exportando resultados...".center(width))
                    lineador()
                    print("¿Qué desea exportar?".center(width))
                    print("1) Base de datos de precios")
                    print("2) Estadísticos de los precios")
                    lineador()
                    while True:
                        try:
                            opcion_export = int(input("Seleccione una opción: "))
                            if opcion_export == 1:
                                nombre_archivo = input("Ingrese el nombre del archivo JSON: ").strip()
                                ruta = exportar_base_json(df_prices, nombre_archivo)
                                lineador()
                                print(f"Base de precios exportada en: {ruta}")
                                lineador()
                                break
                            elif opcion_export == 2:
                                if data_limpia == 0:
                                    lineador()
                                    print("Primero deb calcular los estadisticos de precios")
                                    lineador()
                                    break
                                estadisticos = cal_estadisticos(df_prices, df_assets)
                                nombre_archivo = input("Ingrese el nombre del archivo JSON: ").strip()
                                ruta = exportar_estadisticos_json(estadisticos, nombre_archivo)
                                lineador()
                                print(f"Estadísticos de precios exportados en: {ruta}")
                                lineador()
                                break
                            else:
                                print("Por favor, elija una opción válida")
                                continue
                            
                        except ValueError:
                            print("Elija una opción válida")
                    if retornos_creados == 1:
                        lineador()
                        print("¿Desea exportar retornos?".center(width))
                        print("1) Base de datos de los retornos")
                        print("2) Estadísticos de los retornos")
                        print("3) No exportar retornos")
                        lineador()

                        while True:
                            try:
                                opcion_export_ret = int(input("Seleccione una opción: "))
                                if opcion_export_ret == 1:
                                    nombre_archivo = input("Ingrese el nombre del archivo JSON: ").strip()
                                    ruta = exportar_base_json(df_rets, nombre_archivo)
                                    lineador()
                                    print(f"Base de retornos exportada en: {ruta}")
                                    lineador()
                                    break
                                elif opcion_export_ret == 2:
                                    nombre_archivo = input("Ingrese el nombre del archivo JSON: ").strip()
                                    ruta = exportar_estadisticos_json(estadisticos_rets, nombre_archivo)
                                    lineador()
                                    print(f"Estadísticos de retornos exportados en: {ruta}")
                                    lineador()
                                    break
                                elif opcion_export_ret == 3:
                                    lineador()
                                    print("No se exportarán retornos".center(width))
                                    lineador()
                                    break
                                else:
                                    print("Por favor, elija una opción válida")
                                    continue
                            except ValueError:
                                print("Por favor elija una opción válida".center(width))
                                continue

                except NameError:
                    lineador()
                    print("No hay data cargada")
                    lineador()
                    continue
            
            elif opcion == 7:
                print("Nos vemos pronto ! :)".center(width))
                print("Finalizando programa...".center(width))
                lineador()
                break
            else:
                print("Error, por favor seleccione una opción válida".center(width))
                lineador()
                continue
        except ValueError:
            print("Por favor, seleccione un número dentro de las opciones")
            lineador()
        

if __name__ == "__main__":
    main()