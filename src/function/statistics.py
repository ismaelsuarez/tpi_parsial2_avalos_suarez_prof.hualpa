"""Cálculo e impresión de estadísticas sobre una lista de autos.

Este módulo resume información general (máximos, mínimos, promedios y
cantidad por diferentes criterios) a partir de una lista de diccionarios que
representan autos.
"""

from function.tools import normalizar


def contar_autos_por_marca_recursivo(autos, indice=0, conteo=None):
    """Cuenta autos por marca de forma recursiva.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        autos (list[dict]): Lista de autos.
        indice (int): Índice actual en la lista (para recursión).
        conteo (dict): Diccionario acumulativo de conteos.

    Returns:
        dict: Diccionario con marcas como claves y cantidad de autos como valores.
    """
    if conteo is None:
        conteo = {}

    # Caso base: se recorrió toda la lista
    if indice >= len(autos):
        return conteo

    # Procesar el elemento actual
    auto_actual = autos[indice]
    marca = auto_actual.get("Marca", "Desconocida")
    conteo[marca] = conteo.get(marca, 0) + 1

    # Llamada recursiva para el siguiente elemento
    return contar_autos_por_marca_recursivo(autos, indice + 1, conteo)


def contar_autos_por_combustible_recursivo(autos, indice=0, conteo=None):
    """Cuenta autos por tipo de combustible de forma recursiva.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        autos (list[dict]): Lista de autos.
        indice (int): Índice actual en la lista (para recursión).
        conteo (dict): Diccionario acumulativo de conteos.

    Returns:
        dict: Diccionario con tipos de combustible como claves y cantidad de autos como valores.
    """
    if conteo is None:
        conteo = {}

    # Caso base: se recorrió toda la lista
    if indice >= len(autos):
        return conteo

    # Procesar el elemento actual
    auto_actual = autos[indice]
    combustible = auto_actual.get("TipoCombustible", "Desconocido")
    conteo[combustible] = conteo.get(combustible, 0) + 1

    # Llamada recursiva para el siguiente elemento
    return contar_autos_por_combustible_recursivo(autos, indice + 1, conteo)


def contar_autos_por_transmision_recursivo(autos, indice=0, conteo=None):
    """Cuenta autos por transmisión de forma recursiva.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        autos (list[dict]): Lista de autos.
        indice (int): Índice actual en la lista (para recursión).
        conteo (dict): Diccionario acumulativo de conteos.

    Returns:
        dict: Diccionario con transmisiones como claves y cantidad de autos como valores.
    """
    if conteo is None:
        conteo = {}

    # Caso base: se recorrió toda la lista
    if indice >= len(autos):
        return conteo

    # Procesar el elemento actual
    auto_actual = autos[indice]
    transmision = auto_actual.get("Transmisión", "Desconocida")
    conteo[transmision] = conteo.get(transmision, 0) + 1

    # Llamada recursiva para el siguiente elemento
    return contar_autos_por_transmision_recursivo(autos, indice + 1, conteo)


def sumar_años_recursivo(autos, indice=0):
    """Suma los años de los autos de forma recursiva.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        autos (list[dict]): Lista de autos.
        indice (int): Índice actual en la lista (para recursión).

    Returns:
        int: Suma total de años.
    """
    # Caso base: se recorrió toda la lista
    if indice >= len(autos):
        return 0

    # Procesar el elemento actual
    año_actual = autos[indice].get("Año", 0)

    # Llamada recursiva para el siguiente elemento y sumar
    return año_actual + sumar_años_recursivo(autos, indice + 1)


def mostrar_estadisticas(autos):
    """Imprime estadísticas generales de una lista de autos.

    Calcula y muestra:
      - Auto más antiguo y más nuevo (por año).
      - Promedio de año.
      - Cantidad de autos por marca.
      - Cantidad de autos por tipo de combustible.
      - Cantidad de autos por transmisión.

    La función imprime por consola y no modifica la lista recibida.

    Args:
        autos (list[dict]): Lista de autos. Cada auto debe contener las
            claves:
            - 'Marca' (str)
            - 'Modelo' (str)
            - 'Año' (int)
            - 'TipoCombustible' (str)
            - 'Transmisión' (str)

    Returns:
        None
    """
    if not autos:
        print(" No hay datos disponibles para mostrar estadísticas.")
        return

    # Auto más antiguo y más nuevo
    auto_mas_antiguo = min(autos, key=lambda x: x["Año"])
    auto_mas_nuevo = max(autos, key=lambda x: x["Año"])

    # Promedio de año (usando función recursiva)
    suma_años = sumar_años_recursivo(autos)
    promedio_año = suma_años / len(autos) if autos else 0

    # Conteo por marca (usando función recursiva)
    autos_por_marca = contar_autos_por_marca_recursivo(autos)

    # Conteo por tipo de combustible (usando función recursiva)
    autos_por_combustible = contar_autos_por_combustible_recursivo(autos)

    # Conteo por transmisión (usando función recursiva)
    autos_por_transmision = contar_autos_por_transmision_recursivo(autos)

    print("*********Estadísticas generales*********")
    print(f"▫ 🚗 Auto más antiguo: {auto_mas_antiguo['Marca']} {auto_mas_antiguo['Modelo']} ({auto_mas_antiguo['Año']})")
    print(f"▫ 🚗 Auto más nuevo: {auto_mas_nuevo['Marca']} {auto_mas_nuevo['Modelo']} ({auto_mas_nuevo['Año']})")
    print(f"▫ 📅 Año promedio: {int(promedio_año)}")
    print("")
    print("*********Cantidad de autos por marca*********")
    for marca, cantidad in sorted(autos_por_marca.items()):
        print(f"      - {marca}: {cantidad}")
    print("")
    print("*********Cantidad de autos por tipo de combustible*********")
    for combustible, cantidad in sorted(autos_por_combustible.items()):
        print(f"      - {combustible}: {cantidad}")
    print("")
    print("*********Cantidad de autos por transmisión*********")
    for transmision, cantidad in sorted(autos_por_transmision.items()):
        print(f"      - {transmision}: {cantidad}")
    print("***************************************************")
