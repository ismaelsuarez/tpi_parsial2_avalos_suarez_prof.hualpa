"""Gestión de estructura jerárquica de base de datos.

Este módulo implementa una organización jerárquica de los datos donde:
- autos.csv es el archivo central/maestro
- Los datos se organizan en subcarpetas por diferentes criterios:
  - por_marca/: Subcarpetas con archivos CSV agrupados por marca
  - por_combustible/: Subcarpetas con archivos CSV agrupados por tipo de combustible
  - por_transmision/: Subcarpetas con archivos CSV agrupados por transmisión

Esto permite una organización jerárquica de los datos cumpliendo con los requisitos
del proyecto de tener una estructura de base de datos separada jerárquicamente.
"""

import os
import csv
import shutil
from pathlib import Path


def obtener_ruta_subgrupos(ruta_db_central: str) -> Path:
    """Obtiene la ruta base para los subgrupos jerárquicos.

    Args:
        ruta_db_central (str): Ruta del archivo CSV central (ej: 'src/db/autos.csv').

    Returns:
        Path: Ruta base para los subgrupos (ej: 'src/db/subgrupos').
    """
    db_dir = Path(ruta_db_central).parent
    return db_dir / "subgrupos"


def inicializar_estructura_jerarquica(ruta_db_central: str) -> None:
    """Inicializa la estructura jerárquica de carpetas para subgrupos.

    Crea las carpetas base para organizar datos por marca, combustible y transmisión.

    Args:
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)

    # Crear estructura de carpetas jerárquica
    carpetas = [
        base_subgrupos / "por_marca",
        base_subgrupos / "por_combustible",
        base_subgrupos / "por_transmision",
    ]

    for carpeta in carpetas:
        carpeta.mkdir(parents=True, exist_ok=True)


def limpiar_nombre_archivo(nombre: str) -> str:
    """Limpia un nombre para usarlo como nombre de archivo.

    Elimina caracteres especiales y normaliza espacios.

    Args:
        nombre (str): Nombre a limpiar.

    Returns:
        str: Nombre limpio para archivo.
    """
    # Reemplazar caracteres problemáticos
    nombre = nombre.replace("/", "-").replace("\\", "-")
    nombre = nombre.replace(":", "-").replace("*", "-")
    nombre = nombre.replace("?", "-").replace('"', "-")
    nombre = nombre.replace("<", "-").replace(">", "-")
    nombre = nombre.replace("|", "-").strip()
    return nombre if nombre else "SinNombre"


def organizar_por_marca(autos: list[dict], ruta_db_central: str) -> None:
    """Organiza los autos en subcarpetas agrupados por marca.

    Crea archivos CSV en subcarpetas por_marca/ organizados por marca.

    Args:
        autos (list[dict]): Lista de autos a organizar.
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)
    carpeta_marca = base_subgrupos / "por_marca"

    # Agrupar autos por marca
    autos_por_marca = {}
    for auto in autos:
        marca = auto.get("Marca", "Desconocida")
        if marca not in autos_por_marca:
            autos_por_marca[marca] = []
        autos_por_marca[marca].append(auto)

    # Crear archivo CSV para cada marca
    for marca, lista_autos in autos_por_marca.items():
        nombre_archivo = limpiar_nombre_archivo(marca) + ".csv"
        ruta_archivo = carpeta_marca / nombre_archivo

        fieldnames = ["Marca", "Modelo", "Año", "TipoCombustible", "Transmisión"]
        with open(ruta_archivo, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in lista_autos:
                writer.writerow({
                    "Marca": str(a["Marca"]),
                    "Modelo": str(a["Modelo"]),
                    "Año": int(a["Año"]),
                    "TipoCombustible": str(a["TipoCombustible"]),
                    "Transmisión": str(a["Transmisión"]),
                })


def organizar_por_combustible(autos: list[dict], ruta_db_central: str) -> None:
    """Organiza los autos en subcarpetas agrupados por tipo de combustible.

    Crea archivos CSV en subcarpetas por_combustible/ organizados por combustible.

    Args:
        autos (list[dict]): Lista de autos a organizar.
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)
    carpeta_combustible = base_subgrupos / "por_combustible"

    # Agrupar autos por tipo de combustible
    autos_por_combustible = {}
    for auto in autos:
        combustible = auto.get("TipoCombustible", "Desconocido")
        if combustible not in autos_por_combustible:
            autos_por_combustible[combustible] = []
        autos_por_combustible[combustible].append(auto)

    # Crear archivo CSV para cada tipo de combustible
    for combustible, lista_autos in autos_por_combustible.items():
        nombre_archivo = limpiar_nombre_archivo(combustible) + ".csv"
        ruta_archivo = carpeta_combustible / nombre_archivo

        fieldnames = ["Marca", "Modelo", "Año", "TipoCombustible", "Transmisión"]
        with open(ruta_archivo, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in lista_autos:
                writer.writerow({
                    "Marca": str(a["Marca"]),
                    "Modelo": str(a["Modelo"]),
                    "Año": int(a["Año"]),
                    "TipoCombustible": str(a["TipoCombustible"]),
                    "Transmisión": str(a["Transmisión"]),
                })


def organizar_por_transmision(autos: list[dict], ruta_db_central: str) -> None:
    """Organiza los autos en subcarpetas agrupados por transmisión.

    Crea archivos CSV en subcarpetas por_transmision/ organizados por transmisión.

    Args:
        autos (list[dict]): Lista de autos a organizar.
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)
    carpeta_transmision = base_subgrupos / "por_transmision"

    # Agrupar autos por transmisión
    autos_por_transmision = {}
    for auto in autos:
        transmision = auto.get("Transmisión", "Desconocida")
        if transmision not in autos_por_transmision:
            autos_por_transmision[transmision] = []
        autos_por_transmision[transmision].append(auto)

    # Crear archivo CSV para cada transmisión
    for transmision, lista_autos in autos_por_transmision.items():
        nombre_archivo = limpiar_nombre_archivo(transmision) + ".csv"
        ruta_archivo = carpeta_transmision / nombre_archivo

        fieldnames = ["Marca", "Modelo", "Año", "TipoCombustible", "Transmisión"]
        with open(ruta_archivo, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in lista_autos:
                writer.writerow({
                    "Marca": str(a["Marca"]),
                    "Modelo": str(a["Modelo"]),
                    "Año": int(a["Año"]),
                    "TipoCombustible": str(a["TipoCombustible"]),
                    "Transmisión": str(a["Transmisión"]),
                })


def sincronizar_estructura_jerarquica(autos: list[dict], ruta_db_central: str) -> None:
    """Sincroniza la estructura jerárquica completa con los datos actuales.

    Esta función:
    1. Inicializa la estructura de carpetas si no existe
    2. Organiza los datos en subcarpetas por marca, combustible y transmisión
    3. Mantiene la sincronización entre el archivo central y los subgrupos

    Args:
        autos (list[dict]): Lista completa de autos desde el archivo central.
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    # Inicializar estructura si no existe
    inicializar_estructura_jerarquica(ruta_db_central)

    # Organizar datos en subgrupos jerárquicos
    organizar_por_marca(autos, ruta_db_central)
    organizar_por_combustible(autos, ruta_db_central)
    organizar_por_transmision(autos, ruta_db_central)


def leer_desde_subgrupo(ruta_subgrupo: str) -> list[dict]:
    """Lee autos desde un archivo CSV de un subgrupo jerárquico.

    Args:
        ruta_subgrupo (str): Ruta al archivo CSV del subgrupo.

    Returns:
        list[dict]: Lista de autos leídos del subgrupo.
    """
    autos = []
    if not os.path.exists(ruta_subgrupo):
        return autos

    with open(ruta_subgrupo, "r", encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            marca = fila.get("Marca") or fila.get("marca")
            modelo = fila.get("Modelo") or fila.get("modelo")
            año = fila.get("Año") or fila.get("Año") or fila.get("año")
            tipo_combustible = fila.get("TipoCombustible") or fila.get("tipoCombustible") or fila.get("tipocombustible")
            transmision = fila.get("Transmisión") or fila.get("transmisión") or fila.get("transmision") or fila.get("Transmision")

            if not (marca and modelo and año and tipo_combustible and transmision):
                continue

            try:
                año_int = int(float(año))
            except (TypeError, ValueError):
                continue

            autos.append({
                "Marca": marca.strip(),
                "Modelo": modelo.strip(),
                "Año": año_int,
                "TipoCombustible": tipo_combustible.strip(),
                "Transmisión": transmision.strip(),
            })

    return autos


def obtener_info_estructura_jerarquica(ruta_db_central: str) -> dict:
    """Obtiene información sobre la estructura jerárquica actual.

    Args:
        ruta_db_central (str): Ruta del archivo CSV central.

    Returns:
        dict: Diccionario con información sobre la estructura jerárquica.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)

    info = {
        "ruta_base": str(base_subgrupos),
        "por_marca": {},
        "por_combustible": {},
        "por_transmision": {},
    }

    # Contar archivos en cada subcarpeta
    for tipo in ["por_marca", "por_combustible", "por_transmision"]:
        carpeta = base_subgrupos / tipo
        if carpeta.exists():
            archivos = list(carpeta.glob("*.csv"))
            info[tipo] = {
                "cantidad_archivos": len(archivos),
                "archivos": [arch.name for arch in archivos],
            }
        else:
            info[tipo] = {
                "cantidad_archivos": 0,
                "archivos": [],
            }

    return info

