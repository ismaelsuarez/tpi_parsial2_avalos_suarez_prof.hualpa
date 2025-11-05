"""Inicialización y verificación del archivo CSV de autos.

Este módulo se encarga de ubicar, mover o crear el archivo `autos.csv`
necesario para el modo local. Si el archivo no está en la ruta esperada,
lo busca en todo el proyecto; si lo encuentra en otra carpeta, lo mueve a
la ruta correcta; y si no existe, lo crea con el encabezado por defecto.

Usa utilidades de `function.tools` (por ejemplo, `limpiar_consola`) y
muestra mensajes informativos por consola durante el proceso.
"""

import os
import shutil
import csv
from function.tools import *


def gestionar_db(directorio_base, ruta_objetivo):
    """Verifica, busca, mueve o crea el archivo `autos.csv`.

    Flujo:
        1) Si `ruta_objetivo` ya existe como archivo, la devuelve.
        2) Si no existe, recorre `directorio_base` buscando `autos.csv`.
           - Si lo encuentra en otra ubicación, lo mueve a `ruta_objetivo`.
           - Si ya está en la ubicación correcta, la devuelve.
        3) Si no lo encuentra, crea un CSV nuevo con el encabezado:
           Marca, Modelo, Año, TipoCombustible, Transmisión.

    Args:
        directorio_base (str): Directorio raíz del proyecto donde se realizará
            la búsqueda recursiva.
        ruta_objetivo (str): Ruta donde *debe* estar el CSV (se normaliza).

    Returns:
        str | None: Ruta normalizada del archivo CSV listo para usar, o None
        si ocurrió un error al mover/crear.

    Side effects:
        - Limpia/Imprime por consola el estado de la operación.
        - Puede crear directorios intermedios y mover archivos.

    Nota:
        Cualquier excepción durante el movimiento/creación se captura y se
        informa por consola, devolviendo None.
    """
    ruta_objetivo_norm = os.path.normpath(ruta_objetivo)

    if os.path.isfile(ruta_objetivo_norm):
        limpiar_consola()
        print("******************************")
        print(f"🆙 Iniciando aplicacion...")
        print(f"✅ Sistema cargado")
        return ruta_objetivo_norm

    limpiar_consola()
    print("************************************************************************************")
    print(f"Archivo no encontrado en '{ruta_objetivo_norm}'.")
    print(f"Buscando en todo el proyecto ('{directorio_base}')...")
    ruta_encontrada = None

    for dirpath, dirnames, filenames in os.walk(directorio_base):
        if "autos.csv" in filenames:
            ruta_encontrada = os.path.normpath(os.path.join(dirpath, "autos.csv"))

            if ruta_encontrada != ruta_objetivo_norm:
                limpiar_consola()
                print("****************************************************")
                print("⚠️ ¡Archivo encontrado en una ubicación incorrecta! ")
                try:
                    os.makedirs(os.path.dirname(ruta_objetivo_norm), exist_ok=True)
                    shutil.move(ruta_encontrada, ruta_objetivo_norm)

                    print(f"📦 Archivo movido exitosamente a: {ruta_objetivo_norm}")
                    print("****************************************************")
                    print(f"🆙 Iniciando aplicacion...")
                    print(f"✅ Sistema cargado")
                    return ruta_objetivo_norm

                except Exception as e:
                    print(f"❌ ERROR: No se pudo mover el archivo. Error: {e}")
                    return None
            else:
                print(f"✅ Archivo 'autos.csv' localizado en la ruta correcta: {ruta_encontrada}")
                return ruta_encontrada

    print(f"❌ ERROR: El archivo 'autos.csv' no se encontró en ningún directorio del proyecto.")
    print(f"Creando archivo en la ruta objetivo: {ruta_objetivo_norm}")
    try:
        os.makedirs(os.path.dirname(ruta_objetivo_norm), exist_ok=True)
        with open(ruta_objetivo_norm, 'w', newline='', encoding='utf-8-sig') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerow(["Marca", "Modelo", "Año", "TipoCombustible", "Transmisión"])
        print(f"📄 Archivo 'autos.csv' creado correctamente en: {ruta_objetivo_norm} ")
        print("Se creo solo con su encabezado Marca, Modelo, Año, TipoCombustible, Transmisión")
        print("Por favor, ingresar los datos manualmente en el archivo csv.")
        print("************************************************************************************")
        print(f"✅ Iniciando aplicacion")
        return ruta_objetivo_norm
    except Exception as e:
        print("****************************************************")
        print(f"❌ ERROR: No se pudo crear el archivo. Error: {e}")
        return None


RUTA_CORRECTA_DB = 'src/db/autos.csv'


def init_db(project_root):
    """Prepara la base local (CSV) y devuelve su ruta para uso de la app.

    Esta función es un envoltorio de `gestionar_db`, fijando la ruta esperada
    (`RUTA_CORRECTA_DB`) y devolviendo la ruta final lista para trabajar.

    Args:
        project_root (str): Ruta absoluta a la raíz del proyecto.

    Returns:
        str | None: Ruta final del CSV si todo salió bien, o None si falló.
    """
    db_path = gestionar_db(project_root, RUTA_CORRECTA_DB)
    if db_path is None:
        print("****************************************************")
        print("No se pudo preparar la base de datos. Saliendo.")
        return None
    return db_path
