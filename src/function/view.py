"""Vistas y utilidades de presentación para listas de autos.

Incluye funciones para:
- Mostrar autos en consola con campos básicos.
- Pedir un rango numérico (mínimo y máximo) por consola.
- Ordenar listas de autos por marca, modelo, año, tipo de combustible o transmisión.
"""

import csv  # (opcional: se podría eliminar si no se usa)
from function.tools import normalizar
import unicodedata  # (opcional: no se usa aquí directamente)


def mostrar_autos_recursivo(lista_autos, indice=0):
    """Muestra los autos de forma recursiva.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        lista_autos (list[dict]): Lista de autos a mostrar.
        indice (int): Índice actual en la lista (para recursión).
    """
    # Caso base: se recorrió toda la lista
    if indice >= len(lista_autos):
        return

    # Procesar el elemento actual
    a = lista_autos[indice]
    print(
        f"{a['Marca']} {a['Modelo']} | "
        f"Año: {a['Año']} | "
        f"Combustible: {a['TipoCombustible']} | "
        f"Transmisión: {a['Transmisión']}"
    )

    # Llamada recursiva para el siguiente elemento
    mostrar_autos_recursivo(lista_autos, indice + 1)


def mostrar_autos(lista_autos):
    """Imprime una lista de autos con sus datos principales.

    Esta función utiliza la implementación recursiva internamente.

    Cada elemento de `lista_autos` debe ser un diccionario con las claves:
    'Marca', 'Modelo', 'Año', 'TipoCombustible', 'Transmisión'.

    Args:
        lista_autos (list[dict]): Lista de autos a mostrar.

    Returns:
        None
    """
    if not lista_autos:
        return

    # Usar función recursiva
    mostrar_autos_recursivo(lista_autos)


def pedir_rango(nombre_campo):
    """Solicita por consola un rango (mínimo y máximo) para un campo numérico.

    Muestra dos `input()`: uno para el mínimo y otro para el máximo. Si el
    usuario ingresa un valor no numérico, informa el error y devuelve
    `(None, None)`.

    Args:
        nombre_campo (str): Nombre del campo a pedir (p. ej., 'año').

    Returns:
        tuple[int | None, int | None]: `(minimo, maximo)` si ambos son válidos;
        en caso de error, `(None, None)`.
    """
    try:
        minimo = int(input(f"Ingresá {nombre_campo} mínimo: "))
        maximo = int(input(f"Ingresá {nombre_campo} máximo: "))
        return minimo, maximo
    except ValueError:
        print("Entrada inválida. Debés ingresar números.")
        # Ajuste menor: devolvemos una tupla de dos elementos para evitar errores
        return None, None


def ordenar_autos(autos, campo, descendente=False):
    """Ordena e imprime autos por 'Marca', 'Modelo', 'Año', 'TipoCombustible' o 'Transmisión'.

    La detección del campo es tolerante:
      - Si `campo` contiene "marca" → ordena por Marca.
      - Si `campo` contiene "modelo" → ordena por Modelo.
      - Si `campo` contiene "año" → ordena por Año.
      - Si `campo` contiene "combustible" o "tipo" → ordena por TipoCombustible.
      - Si `campo` contiene "transmision" → ordena por Transmisión.

    Para campos de texto se usa orden lexicográfico por versión normalizada (sin
    acentos y en minúsculas). Para 'Año' se ordena numéricamente.

    Args:
        autos (list[dict]): Lista de autos a ordenar y mostrar.
        campo (str): Criterio de orden: marca/modelo/año/tipocombustible/transmision (o subcadenas).
        descendente (bool): Si es True, orden descendente.

    Returns:
        None
    """
    try:
        campo_norm = normalizar(campo)

        if "marca" in campo_norm:
            campo_orden = "Marca"
        elif "modelo" in campo_norm:
            campo_orden = "Modelo"
        elif "año" in campo_norm or "ano" in campo_norm:
            campo_orden = "Año"
        elif "combustible" in campo_norm or "tipo" in campo_norm:
            campo_orden = "TipoCombustible"
        elif "transmision" in campo_norm:
            campo_orden = "Transmisión"
        else:
            print("Campo inválido para ordenar. Usá: marca / modelo / año / tipocombustible / transmision.")
            return

        if campo_orden in ["Marca", "Modelo", "TipoCombustible", "Transmisión"]:
            autos_ordenados = sorted(
                autos,
                key=lambda x: normalizar(str(x[campo_orden])),
                reverse=descendente,
            )
        elif campo_orden == "Año":
            autos_ordenados = sorted(
                autos,
                key=lambda x: x[campo_orden],
                reverse=descendente,
            )
        else:
            print("Campo inválido para ordenar.")
            return

        print(
            f"\nAutos ordenados por {campo_orden} "
            f"({'descendente' if descendente else 'ascendente'}):"
        )
        mostrar_autos(autos_ordenados)

    except Exception as e:
        print(f"Error al ordenar: {e}")
