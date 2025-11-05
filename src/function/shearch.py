"""Búsquedas y filtros para autos (modo local).

Este módulo proporciona funciones para buscar y filtrar autos por diferentes criterios:
- Búsqueda por marca o modelo
- Filtro por tipo de combustible
- Filtro por rango de año
- Filtro por transmisión
"""

import csv
from function.tools import *
from function.view import *


def _leer_entero_no_negativo(respuesta: str):
    """
    Lee desde input y valida:
    - solo dígitos (isdigit) -> sin letras, sin espacios, sin signos
    - entero no negativo
    Devuelve int o None si es inválido.
    """
    s = input(respuesta).strip()
    if not s.isdigit():
        print("Ingrese solo números enteros no negativos (sin espacios ni letras).")
        return None
    return int(s)


def buscar_auto(autos, busqueda):
    """Busca autos por marca o modelo.

    Args:
        autos (list[dict]): Lista de autos donde buscar.
        busqueda (str): Texto a buscar en Marca o Modelo (no case-sensitive, sin acentos).

    Returns:
        None (imprime resultados por consola).
    """
    busqueda_norm = normalizar(busqueda)
    encontrados = [
        a for a in autos
        if busqueda_norm in normalizar(a["Marca"]) or busqueda_norm in normalizar(a["Modelo"])
    ]

    if encontrados:
        print(f"\nSe encontraron {len(encontrados)} auto(s):")
        mostrar_autos(encontrados)
    else:
        print("No se encontró ningún auto con esa marca o modelo.")


def filtrar_combustible(autos, tipo_combustible):
    """Filtra autos por tipo de combustible.

    Args:
        autos (list[dict]): Lista de autos a filtrar.
        tipo_combustible (str): Tipo de combustible a buscar.

    Returns:
        None (imprime resultados por consola).
    """
    tipo_norm = normalizar(tipo_combustible)
    resultados = [
        a for a in autos
        if tipo_norm in normalizar(a["TipoCombustible"])
    ]
    if resultados:
        print(f"\n Autos con tipo de combustible '{tipo_combustible}':")
        mostrar_autos(resultados)
    else:
        print(f"\n No se encontraron autos con tipo de combustible '{tipo_combustible}'.")


def filtrar_año(autos):
    """Filtra autos por rango de año.

    Solicita al usuario el año mínimo y máximo, y muestra los autos que
    se encuentran en ese rango.

    Args:
        autos (list[dict]): Lista de autos a filtrar.

    Returns:
        None (imprime resultados por consola).
    """
    minimo = _leer_entero_no_negativo("Ingrese el año mínimo: ")
    if minimo is None:
        return
    maximo = _leer_entero_no_negativo("Ingrese el año máximo: ")
    if maximo is None:
        return

    if minimo > maximo:
        print("El mínimo no puede ser mayor que el máximo.")
        return

    resultado = [
        a for a in autos
        if minimo <= a.get('Año', -1) <= maximo
    ]

    if resultado:
        print(f"\nAutos con año entre {minimo} y {maximo}:")
        mostrar_autos(resultado)
    else:
        print("No se encontraron autos en ese rango de año.")


def filtrar_transmision(autos, transmision):
    """Filtra autos por tipo de transmisión.

    Args:
        autos (list[dict]): Lista de autos a filtrar.
        transmision (str): Tipo de transmisión a buscar (Manual o Automática).

    Returns:
        None (imprime resultados por consola).
    """
    transmision_norm = normalizar(transmision)
    resultados = [
        a for a in autos
        if transmision_norm in normalizar(a["Transmisión"])
    ]
    if resultados:
        print(f"\n Autos con transmisión '{transmision}':")
        mostrar_autos(resultados)
    else:
        print(f"\n No se encontraron autos con transmisión '{transmision}'.")