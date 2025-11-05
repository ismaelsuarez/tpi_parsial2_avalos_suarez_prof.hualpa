"""Cálculo e impresión de estadísticas sobre una lista de autos.

Este módulo resume información general (máximos, mínimos, promedios y
cantidad por diferentes criterios) a partir de una lista de diccionarios que
representan autos.
"""

from function.tools import normalizar


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

    # Promedio de año
    promedio_año = sum(a["Año"] for a in autos) / len(autos)

    # Conteo por marca
    autos_por_marca = {}
    for a in autos:
        marca = a["Marca"]
        autos_por_marca[marca] = autos_por_marca.get(marca, 0) + 1

    # Conteo por tipo de combustible
    autos_por_combustible = {}
    for a in autos:
        combustible = a["TipoCombustible"]
        autos_por_combustible[combustible] = autos_por_combustible.get(combustible, 0) + 1

    # Conteo por transmisión
    autos_por_transmision = {}
    for a in autos:
        transmision = a["Transmisión"]
        autos_por_transmision[transmision] = autos_por_transmision.get(transmision, 0) + 1

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
