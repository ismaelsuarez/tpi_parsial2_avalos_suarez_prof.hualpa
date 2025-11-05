"""Operaciones locales (modo archivo) para gestionar autos.

Este módulo implementa altas, ediciones y borrados sobre la lista `autos`
en memoria, solicitando los datos por consola y reutilizando utilidades de
`function.tools` (por ejemplo, `normalizar`).
"""

from function.tools import *


def agregar_auto(autos):
    """Agrega un auto a la lista en memoria solicitando datos por consola.

    Pide Marca, Modelo, Año, TipoCombustible y Transmisión, valida que los
    campos requeridos no estén vacíos y agrega un diccionario con esos datos a
    la lista `autos`.

    Args:
        autos (list[dict]): Lista mutable de autos donde se insertará el nuevo
            registro. Cada auto es un dict con claves:
            `Marca` (str), `Modelo` (str), `Año` (int), `TipoCombustible` (str),
            `Transmisión` (str).

    Returns:
        None
    """
    print("\n--- Agregar nuevo auto ---")

    marca = input("Marca del auto: ").strip()
    while marca == "":
        marca = input(
            "La marca no puede estar vacía. Ingresá nuevamente: "
        ).strip()

    modelo = input("Modelo del auto: ").strip()
    while modelo == "":
        modelo = input(
            "El modelo no puede estar vacío. Ingresá nuevamente: "
        ).strip()

    try:
        año = int(input("Año: "))
        while año < 1900 or año > 2100:
            año = int(input("Año inválido. Ingresá un año entre 1900 y 2100: "))
    except ValueError:
        print("Error: El año debe ser numérico.")
        return

    tipo_combustible = input("Tipo de combustible (Nafta, Diesel, Híbrido, Eléctrico): ").strip()
    while tipo_combustible == "":
        tipo_combustible = input(
            "El tipo de combustible no puede estar vacío. Ingresá nuevamente: "
        ).strip()

    transmision = input("Transmisión (Manual, Automática): ").strip()
    while transmision == "":
        transmision = input(
            "La transmisión no puede estar vacía. Ingresá nuevamente: "
        ).strip()

    nuevo_auto = {
        "Marca": marca,
        "Modelo": modelo,
        "Año": año,
        "TipoCombustible": tipo_combustible,
        "Transmisión": transmision,
    }

    autos.append(nuevo_auto)
    print(f"Auto '{marca} {modelo}' agregado correctamente.")


def editar_auto(autos):
    """Modifica los datos de un auto existente (modo local).

    Muestra coincidencias por marca o modelo y permite seleccionar una para
    actualizar sus campos.

    Args:
        autos (list[dict]): Lista mutable de autos. Se modifica in-place.

    Returns:
        None
    """
    print("\n--- Editar auto ---")
    busqueda = input("Ingresá la marca o modelo del auto que querés editar: ").strip()
    if not busqueda:
        print("Búsqueda vacía, cancelado.")
        return

    busqueda_norm = normalizar(busqueda)
    resultados = [
        a for a in autos
        if busqueda_norm in normalizar(a["Marca"]) or busqueda_norm in normalizar(a["Modelo"])
    ]

    if not resultados:
        print(f" No se encontró ningún auto que contenga '{busqueda}'.")
        return

    print(f"\nSe encontraron {len(resultados)} auto(s):")
    for i, a in enumerate(resultados, 1):
        print(
            f"{i}. {a['Marca']} {a['Modelo']} | "
            f"Año: {a['Año']} | "
            f"Combustible: {a['TipoCombustible']} | "
            f"Transmisión: {a['Transmisión']}"
        )

    try:
        indice = int(input("Elegí el número del auto que querés editar: ")) - 1
        if indice < 0 or indice >= len(resultados):
            print(" Número inválido.")
            return

        auto = resultados[indice]

        print(f"\nEditando: {auto['Marca']} {auto['Modelo']}")
        print("(Presiona Enter para mantener el valor actual)")

        nueva_marca = input(f"Nueva marca [{auto['Marca']}]: ").strip()
        if nueva_marca:
            auto["Marca"] = nueva_marca

        nuevo_modelo = input(f"Nuevo modelo [{auto['Modelo']}]: ").strip()
        if nuevo_modelo:
            auto["Modelo"] = nuevo_modelo

        try:
            nuevo_año = input(f"Nuevo año [{auto['Año']}]: ").strip()
            if nuevo_año:
                año_int = int(nuevo_año)
                if 1900 <= año_int <= 2100:
                    auto["Año"] = año_int
                else:
                    print("Año inválido. Se mantiene el valor anterior.")
        except ValueError:
            print("Año inválido. Se mantiene el valor anterior.")

        nuevo_combustible = input(f"Nuevo tipo de combustible [{auto['TipoCombustible']}]: ").strip()
        if nuevo_combustible:
            auto["TipoCombustible"] = nuevo_combustible

        nueva_transmision = input(f"Nueva transmisión [{auto['Transmisión']}]: ").strip()
        if nueva_transmision:
            auto["Transmisión"] = nueva_transmision

        print(f"Datos actualizados para {auto['Marca']} {auto['Modelo']}.")

    except ValueError:
        print("Entrada inválida.")


def borrar_auto(autos) -> bool:
    """Elimina un auto de la lista en memoria (modo local) por selección.

    Flujo:
        1) Solicita marca o modelo (o parte) y busca coincidencias.
        2) Muestra los candidatos y pide elegir uno por índice (1..n).
        3) Solicita confirmación y elimina de `autos`.

    Args:
        autos (list[dict]): Lista mutable de autos de la que se eliminará
            el registro seleccionado.

    Returns:
        bool: True si se eliminó, False si se canceló o no hubo selección válida.
    """
    print("\n--- Borrar auto (LOCAL) ---")
    busqueda = input("Ingresá la marca o modelo del auto (o parte): ").strip()
    if not busqueda:
        print("Búsqueda vacía, cancelado.")
        return False

    busqueda_norm = normalizar(busqueda)
    resultados = [
        a for a in autos
        if busqueda_norm in normalizar(a["Marca"]) or busqueda_norm in normalizar(a["Modelo"])
    ]

    if not resultados:
        print(f"No se encontró ningún auto que contenga '{busqueda}'.")
        return False

    print(f"\nSe encontraron {len(resultados)} auto(s):")
    for i, a in enumerate(resultados, 1):
        print(
            f"{i}. {a['Marca']} {a['Modelo']} | "
            f"Año: {a['Año']} | "
            f"Combustible: {a['TipoCombustible']} | "
            f"Transmisión: {a['Transmisión']}"
        )

    try:
        idx = int(input("Elegí el número del auto a borrar: ").strip()) - 1
        if idx < 0 or idx >= len(resultados):
            print("Número inválido.")
            return False
    except ValueError:
        print("Entrada inválida.")
        return False

    objetivo = resultados[idx]
    confirma = (
        input(f"Confirmás borrar '{objetivo['Marca']} {objetivo['Modelo']}'? (s/n): ")
        .strip()
        .lower()
        == "s"
    )
    if not confirma:
        print("Operación cancelada.")
        return False

    # Buscar y eliminar de la lista original
    for i, a in enumerate(autos):
        if (a["Marca"] == objetivo["Marca"] and
            a["Modelo"] == objetivo["Modelo"] and
            a["Año"] == objetivo["Año"]):
            autos.pop(i)
            print(f"'{objetivo['Marca']} {objetivo['Modelo']}' borrado correctamente (LOCAL).")
            return True

    print("No se pudo ubicar el registro en la lista original.")
    return False
