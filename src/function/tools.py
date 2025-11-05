"""Utilidades comunes para el modo local y modo API.

Incluye:
- Normalización de texto (elimina acentos, espacios extremos y pasa a minúsculas).
- Lectura y escritura de autos en CSV.
- Ayudas de consola (limpiar pantalla, menús, mensajes y errores).
"""

import unicodedata
import csv
import os


def normalizar(texto):
    """Devuelve el texto en minúsculas, sin espacios extremos ni acentos.

    Usa normalización Unicode (NFD) para remover marcas diacríticas.

    Args:
        texto (str): Cadena de entrada.

    Returns:
        str: Texto normalizado en minúsculas y sin acentos.
    """
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


def leer_csv(ruta_csv: str):
    """Lee un CSV de autos y devuelve una lista de dicts.

    La función es tolerante a encabezados alternativos. Si encuentra
    filas con datos faltantes o no numéricos donde corresponde, las omite y
    muestra un aviso. Si no se obtiene ninguna fila válida, informa que el
    CSV puede estar dañado.

    Campos esperados por fila:
        - Marca (str)
        - Modelo (str)
        - Año (int)   [se castea desde texto]
        - TipoCombustible (str)
        - Transmisión (str)

    Args:
        ruta_csv (str): Ruta al archivo CSV con codificación UTF-8 (BOM ok).

    Returns:
        list[dict]: Lista de autos válidos leídos del archivo.
    """
    autos = []
    filas_invalidas = 0

    with open(ruta_csv, "r", encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            marca = fila.get("Marca") or fila.get("marca")
            modelo = fila.get("Modelo") or fila.get("modelo")
            año = fila.get("Año") or fila.get("Año") or fila.get("año")
            tipo_combustible = fila.get("TipoCombustible") or fila.get("tipoCombustible") or fila.get("tipocombustible")
            transmision = fila.get("Transmisión") or fila.get("transmisión") or fila.get("transmision") or fila.get("Transmision")

            # Validación básica de presencia
            if not (marca and modelo and año and tipo_combustible and transmision):
                filas_invalidas += 1
                continue

            # Parseos numéricos tolerantes
            try:
                año_int = int(float(año))
            except (TypeError, ValueError):
                filas_invalidas += 1
                continue

            autos.append({
                "Marca": marca.strip(),
                "Modelo": modelo.strip(),
                "Año": año_int,
                "TipoCombustible": tipo_combustible.strip(),
                "Transmisión": transmision.strip(),
            })

    if filas_invalidas:
        print("***************************************************************************************")
        print(f"🛑 Se ignoraron {filas_invalidas} fila(s) inválida(s) en {ruta_csv}. archivo dañado")
    if not autos:
        print("🧐 CSV leído, pero no se obtuvieron filas válidas, csv corrupto o dañado")
        print("No tendra datos iterables, cuando cargue un auto se creara una base datos nueva")
        print("****************************************************************************************")
    return autos


def escribir_csv(ruta_csv: str, autos: list[dict]) -> None:
    """Escribe la lista de autos en un CSV con encabezado estándar.

    El archivo se crea/sobrescribe usando UTF-8 con BOM y las columnas:
    'Marca', 'Modelo', 'Año', 'TipoCombustible', 'Transmisión'.

    Además, sincroniza la estructura jerárquica de subgrupos organizando
    los datos en subcarpetas por marca, combustible y transmisión.

    Args:
        ruta_csv (str): Ruta destino del archivo CSV.
        autos (list[dict]): Lista de autos a persistir.

    Returns:
        None
    """
    fieldnames = ["Marca", "Modelo", "Año", "TipoCombustible", "Transmisión"]
    with open(ruta_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for a in autos:
            writer.writerow({
                "Marca": str(a["Marca"]),
                "Modelo": str(a["Modelo"]),
                "Año": int(a["Año"]),
                "TipoCombustible": str(a["TipoCombustible"]),
                "Transmisión": str(a["Transmisión"]),
            })

    # Sincronizar estructura jerárquica después de escribir el archivo central
    try:
        from function.jerarquia import sincronizar_estructura_jerarquica
        sincronizar_estructura_jerarquica(autos, ruta_csv)
    except ImportError:
        # Si el módulo jerarquia no está disponible, continuar sin sincronización
        pass


def limpiar_consola():
    """Limpia la consola según el sistema operativo (cls/clear)."""
    os.system("cls" if os.name == "nt" else "clear")


def salida():
    """Muestra un mensaje de despedida del programa."""
    print("*******************👍************************")
    print("*     Gracias por usar el programa.         *")
    print("*********************************************")


def error_tipeo(op):
    """Informa un error de opción inválida en la selección de modo.

    Args:
        op (Any): Valor ingresado por el usuario.
    """
    print("*******************🛑*************************")
    print(f"*🫣  Opcion incorrecta: ingresaste {op}")
    print("*😁 Recuerda ingresar un numero del 1 al 2")
    print("*******************🛑*************************")


def nube():
    """Imprime información del modo API (servidor nube)."""
    print("**********************************")
    print("🟢  Ingreso por API ")
    print("☁️   Servidor nube ")
    print("🌍  Url: http://149.50.150.15:8010")
    print("***********************************")


def local():
    """Imprime información del modo local (archivos CSV)."""
    print("**********************************")
    print("🟢  Ingreso Modo Local ")
    print("💻  Servidor Fisico ")
    print("***********************************")


def seleccion():
    """Muestra el menú de selección de servidor y devuelve la opción elegida.

    Returns:
        int: 1 para CSV local, 2 para API, 3 para salir.

    Nota:
        Esta función no maneja ValueError de `int(input(...))`. Se espera que
        el llamador capture la excepción si el usuario ingresa texto inválido.
    """
    print("****Seleccione el servidor****")
    print("1. CSV local 💻")
    print("2. CSV  API  ☁️")
    print("3. Salir 🛑")
    op = int(input("Elegí 1 o 2 : "))
    return op


def menu_principal():
    """Muestra el menú principal de operaciones y devuelve la opción elegida.

    Returns:
        int: Número de opción (1 a 11).

    Nota:
        Esta función no maneja ValueError de `int(input(...))`. Se espera que
        el llamador capture la excepción si el usuario ingresa texto inválido.
    """
    print("")
    print("**********GESTIÓN DE AUTOS**********")
    print("1.  Buscar auto por marca o modelo")
    print("2.  Filtrar por tipo de combustible")
    print("3.  Filtrar por rango de año")
    print("4.  Filtrar por transmisión")
    print("5.  Ordenar autos")
    print("6.  Mostrar estadisticas")
    print("7.  Agregar un auto")
    print("8.  Editar un auto")
    print("9.  Borrar auto")
    print("10. Cambiar modo de servidor")
    print("11. Salir")

    opcion = int(input("Ingrese una opcion 1-11: "))
    print("***********************************")
    return opcion


def error_tipeo_menu(opcion):
    """Informa un error de opción inválida en el menú principal.

    Args:
        opcion (Any): Valor ingresado por el usuario.
    """
    print("*******************🛑*************************")
    print(f"*🫣  Opcion incorrecta: ingresaste {opcion}  ")
    print("*😁 Recuerda ingresar un numero del 1 al 11   ")
    print("*******************🛑*************************")


def except_men_server():
    """Mensaje de error cuando la opción del selector de servidor no es numérica."""
    print("***********************🛑*******************************")
    print("*🤔 Opcion incorrecta: No ingresaste un numero valido  *")
    print("*😁      Recuerda ingresar un numero del 1 al 2       *")
    print("***********************🛑*******************************")


def except_men_principal():
    """Mensaje de error cuando la opción del menú principal no es numérica."""
    print("***********************🛑*******************************")
    print("*🤔 Opcion incorrecta: No ingresaste un numero valido  *")
    print("*😁      Recuerda ingresar un numero del 1 al 11       *")
    print("***********************🛑*******************************")


def except_local(e):
    """Mensaje estándar para errores en modo local.

    Args:
        e (Exception): Excepción capturada por el llamador.
    """
    print("*****************************************")
    print("😡 Advertencia: error local:", e)
    print("Intente más tarde o seleccione modo nube")
    print("Disculpe las molestias                   ")
    print("*****************************************")


def error_server():
    """Mensaje estándar para errores al contactar el servidor API."""
    print("*****************************************")
    print("😡 Advertencia: api-server no respondió ")
    print("Intente más tarde o seleccione modo local")
    print("Disculpe las molestias                   ")
    print("*****************************************")
