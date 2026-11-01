def menu1():
    print("menu1")


def menu2():
    print("menu2")


def menu3():
    print("menu3")


print("---------------------------")
print("-------DNS OPTIMIZER-------")
print("---------------------------\n")
print(
    "1. Mostrar conexiones a host especificos"
)  # submenu escoger nombre fichero y ubicacion. (web_<SEMESTRE>.txt)
print(
    "2. Exportar información de Adaptadores de red/MAC"
)  # exportar a informacion_local<Apellido1>.csv + fecha + hora creacion
print(
    "3. Listar configuración de 1 adaptador de red"
)  # mostrar sub menu para escoger si hay varios y exportar a adaptador<Apellido1>.txt
print("Seleciona una opción: del 1 al 3. 0 para salir. ")

opcion = int(input())

if opcion == 1:
    menu1()
elif opcion == 2:
    menu2()
elif opcion == 3:
    menu3()
elif opcion == 0:
    print("Adios.")
else:
    print("Error....")
