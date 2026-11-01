import subprocess
from pathlib import Path


def preguntarFichero():
    fichero = input("Indica el nombre del fichero que contiene los hosts: ")
    return fichero.strip()


def preguntarUbicacion():
    ubicacion = input("Indica la ubicación del fichero: ")
    return ubicacion.strip()


def mostrarFichero(ruta_archivo):
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        print(f"Error: El archivo en '{ruta}' no existe.")
        return

    print(f"\n--- Contenido del archivo: {ruta.name} ---")
    lineas_mostradas = 0

    try:
        with open(ruta, "r", encoding="utf-8-sig") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                print(f"[{numero_linea}] {linea.strip()}")
                lineas_mostradas += 1
    except Exception as error:
        print(f"No se pudo leer el archivo: {error}")
        return

    if lineas_mostradas == 0:
        print("(El archivo está completamente vacío)")
    print("----------------------------------------\n")


def hacerPing(ruta_archivo):
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        print(f"Error: El archivo en '{ruta}' no existe.")
        return

    try:
        with open(ruta, "r", encoding="utf-8-sig") as archivo:
            for linea in archivo:
                ip = linea.strip()
                if ip == "":
                    continue

                print(f"Enviando ping a: {ip}...")
                comando_final = ["ping", "-n", "1", "-w", "1000", ip]
                resultado = subprocess.run(
                    comando_final,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                if resultado.returncode == 0:
                    print(f"{ip} SI responde.\n")
                else:
                    print(f"{ip} NO responde.\n")
    except Exception as error:
        print(f"No se pudo ejecutar el ping o leer el fichero: {error}")


def menu1():
    fichero = preguntarFichero()
    ubicacion = preguntarUbicacion()

    ruta = Path(ubicacion) / fichero

    while True:
        print(f"\nRuta indicada: {ruta}")
        esCorrecta = input("¿Es correcta? s/n: ").strip().lower()

        if esCorrecta == "s":
            mostrarFichero(ruta)
            hacerPing(ruta)
            break
        elif esCorrecta == "n":
            fichero = preguntarFichero()
            ubicacion = preguntarUbicacion()
            ruta = Path(ubicacion) / fichero
        else:
            print("Escribe s para sí o n para no.")


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

opcion = input()

if opcion == "1":
    menu1()
elif opcion == "2":
    menu2()
elif opcion == "3":
    menu3()
elif opcion == "0":
    print("Adios.")
else:
    print("Error....")
