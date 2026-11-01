import csv
import subprocess
from datetime import datetime
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


def obtenerAdaptadores():
    try:
        resultado = subprocess.run(
            ["ipconfig", "/all"],
            capture_output=True,
            text=True,
            encoding="oem",
        )
    except Exception as error:
        print(f"No se pudo ejecutar ipconfig: {error}")
        return []

    adaptadores = []
    adaptador = None

    for linea in resultado.stdout.splitlines():
        texto = linea.strip()

        # Cada bloque de ipconfig comienza con un encabezado Adaptador.
        if texto.startswith("Adaptador "):
            if adaptador is not None:
                adaptadores.append(adaptador)

            nombre = texto.replace("Adaptador de ", "", 1).rstrip(":")
            nombre = nombre.replace("Ethernet ", "", 1)
            nombre = nombre.replace("LAN inalámbrica ", "", 1)
            nombre = nombre.replace("desconocido ", "", 1)
            adaptador = {
                "nombre": nombre,
                "mac": "No disponible",
                "ip": "No configurada",
                "mascara": "No configurada",
                "puerta": "No configurada",
            }

        if adaptador is not None and ":" in texto:
            etiqueta = texto.lower()
            valor = texto.split(":")[-1].strip().split("(")[0].strip()

            if "dirección física" in etiqueta or "physical address" in etiqueta:
                if valor != "":
                    adaptador["mac"] = valor
            elif "ipv4" in etiqueta:
                if valor != "":
                    adaptador["ip"] = valor
            elif "máscara de subred" in etiqueta or "subnet mask" in etiqueta:
                if valor != "":
                    adaptador["mascara"] = valor
            elif (
                "puerta de enlace predeterminada" in etiqueta
                or "default gateway" in etiqueta
            ):
                if valor != "":
                    adaptador["puerta"] = valor

    if adaptador is not None:
        adaptadores.append(adaptador)

    return adaptadores


def listarMAC():
    adaptadores = obtenerAdaptadores()
    if len(adaptadores) == 0:
        print("No se encontraron adaptadores de red.")
        return

    nombre_csv = "informacion_localRigall.csv"
    archivo_nuevo = not Path(nombre_csv).exists()
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        with open(nombre_csv, "a", newline="", encoding="utf-8-sig") as archivo:
            escritor = csv.writer(archivo)
            if archivo_nuevo:
                escritor.writerow(["Fecha y hora", "Adaptador", "Dirección MAC"])

            for adaptador in adaptadores:
                print(f"{adaptador['nombre']}: MAC {adaptador['mac']}")
                escritor.writerow([fecha_hora, adaptador["nombre"], adaptador["mac"]])

        print(f"Información guardada en {nombre_csv}")
    except Exception as error:
        print(f"No se pudo guardar el archivo CSV: {error}")


def menu2():
    listarMAC()


def listarAdaptadores():
    """Muestra los adaptadores disponibles para que el usuario elija uno."""
    adaptadores = obtenerAdaptadores()
    if len(adaptadores) == 0:
        print("No se encontraron adaptadores de red.")
        return []

    print("\nAdaptadores de red disponibles:")
    for numero, adaptador in enumerate(adaptadores, start=1):
        print(f"{numero}. {adaptador['nombre']}")
    return adaptadores


def exportarAdaptador(adaptadorEscogido):
    """Muestra y guarda IP, máscara y puerta de enlace de un adaptador."""
    lineas = [
        f"Adaptador: {adaptadorEscogido['nombre']}",
        f"IP: {adaptadorEscogido['ip']}",
        f"Máscara: {adaptadorEscogido['mascara']}",
        f"Puerta de enlace: {adaptadorEscogido['puerta']}",
    ]

    for linea in lineas:
        print(linea)

    nombre_txt = "adaptadorRigall.txt"
    try:
        with open(nombre_txt, "w", encoding="utf-8") as archivo:
            for linea in lineas:
                archivo.write(linea + "\n")
        print(f"Configuración guardada en {nombre_txt}")
    except Exception as error:
        print(f"No se pudo guardar el archivo TXT: {error}")


def menu3():
    """Pregunta qué adaptador se quiere consultar y guarda sus datos."""
    adaptadores = listarAdaptadores()
    if len(adaptadores) == 0:
        return

    seleccion = input("Selecciona el número del adaptador: ").strip()
    if seleccion.isdigit():
        numero = int(seleccion)
        if numero >= 1 and numero <= len(adaptadores):
            exportarAdaptador(adaptadores[numero - 1])
        else:
            print("El número no corresponde a un adaptador de la lista.")
    else:
        print("Debes escribir un número.")


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
