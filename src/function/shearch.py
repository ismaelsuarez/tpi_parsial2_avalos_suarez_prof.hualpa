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


def buscar_auto_recursivo(autos, busqueda, indice=0, encontrados=None):
    """Busca autos de forma recursiva por marca o modelo.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        autos (list[dict]): Lista de autos donde buscar.
        busqueda (str): Texto a buscar en Marca o Modelo.
        indice (int): Índice actual en la lista (para recursión).
        encontrados (list[dict]): Lista acumulativa de resultados.

    Returns:
        list[dict]: Lista de autos que coinciden con la búsqueda.
    """
    if encontrados is None:
        encontrados = []

    # Caso base: se recorrió toda la lista
    if indice >= len(autos):
        return encontrados

    # Procesar el elemento actual
    auto_actual = autos[indice]
    busqueda_norm = normalizar(busqueda)
    marca_norm = normalizar(auto_actual.get("Marca", ""))
    modelo_norm = normalizar(auto_actual.get("Modelo", ""))

    if busqueda_norm in marca_norm or busqueda_norm in modelo_norm:
        encontrados.append(auto_actual)

    # Llamada recursiva para el siguiente elemento
    return buscar_auto_recursivo(autos, busqueda, indice + 1, encontrados)


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

    Esta función utiliza la implementación recursiva internamente.

    Args:
        autos (list[dict]): Lista de autos donde buscar.
        busqueda (str): Texto a buscar en Marca o Modelo (no case-sensitive, sin acentos).

    Returns:
        None (imprime resultados por consola).
    """
    # Usar búsqueda recursiva
    encontrados = buscar_auto_recursivo(autos, busqueda)

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