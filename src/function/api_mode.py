"""Lógica de modo API para gestionar autos.

Este módulo proporciona funciones para interactuar con la API de autos
usando directamente los campos del CSV: Marca, Modelo, Año, TipoCombustible, Transmisión.
"""

from function.tools import normalizar
from function.view import mostrar_autos, ordenar_autos
from function.statistics import mostrar_estadisticas
from function.shearch import buscar_auto, filtrar_combustible, filtrar_año, filtrar_transmision
from function import api_client


def obtener_autos_api(q=None, tipo_combustible=None, sort_by=None, desc=False):
    """Obtiene autos desde la API con filtros opcionales.

    Args:
        q (str | None): Texto a buscar (busca en Marca o Modelo).
        tipo_combustible (str | None): Filtro por tipo de combustible.
        sort_by (str | None): Campo de ordenamiento (Marca, Modelo, Año, TipoCombustible, Transmisión).
        desc (bool): Si True, orden descendente.

    Returns:
        list[dict]: Lista de autos con estructura: Marca, Modelo, Año, TipoCombustible, Transmisión.
    """
    try:
        items = api_client.listar_autos(
            q=q,
            tipo_combustible=tipo_combustible,
            ordenar_por=sort_by,
            descendente=desc,
        )
        
        # Verificar que items sea una lista
        if not isinstance(items, list):
            print(f"⚠️ Error: La API no devolvió una lista. Tipo recibido: {type(items)}")
            return []
        
        # Verificar si la lista está vacía
        if len(items) == 0:
            print(f"\n⚠️ La API no tiene datos disponibles.")
            print(f"   La API en http://149.50.150.15:8010 está conectada pero no contiene autos.")
            print(f"   Necesitás cargar datos primero usando la opción 'Agregar un auto' del menú.")
            return []
        
        return items
    except Exception as e:
        print(f"⚠️ Error al obtener autos desde la API: {e}")
        import traceback
        traceback.print_exc()
        return []


def buscar_auto_api(busqueda: str):
    """Busca autos por marca o modelo usando la API.

    Args:
        busqueda (str): Texto a buscar.
    """
    autos = obtener_autos_api(q=busqueda)
    if not autos:
        # El mensaje ya se mostró en obtener_autos_api
        return
    buscar_auto(autos, busqueda)


def filtrar_combustible_api(tipo_combustible: str):
    """Filtra autos por tipo de combustible usando la API.

    Args:
        tipo_combustible (str): Tipo de combustible a filtrar.
    """
    autos = obtener_autos_api(tipo_combustible=tipo_combustible)
    if not autos:
        # El mensaje ya se mostró en obtener_autos_api
        return
    filtrar_combustible(autos, tipo_combustible)


def filtrar_año_api():
    """Filtra autos por rango de año usando la API.

    Obtiene todos los autos y luego filtra localmente por rango.
    """
    autos = obtener_autos_api()
    if not autos:
        # El mensaje ya se mostró en obtener_autos_api
        return
    filtrar_año(autos)


def filtrar_transmision_api(transmision: str):
    """Filtra autos por transmisión usando la API.

    Args:
        transmision (str): Tipo de transmisión a filtrar.
    """
    autos = obtener_autos_api()
    if not autos:
        # El mensaje ya se mostró en obtener_autos_api
        return
    # Filtrar localmente porque puede no haber filtro directo en la API
    resultados = [
        a for a in autos
        if normalizar(transmision) in normalizar(a.get("Transmisión", ""))
    ]
    if resultados:
        print(f"\n Autos con transmisión '{transmision}':")
        mostrar_autos(resultados)
    else:
        print(f"\n No se encontraron autos con transmisión '{transmision}'.")


def ordenar_autos_api(campo: str, descendente: bool = False):
    """Ordena autos usando la API.

    Args:
        campo (str): Campo de ordenamiento (Marca, Modelo, Año, TipoCombustible, Transmisión).
        descendente (bool): Si True, orden descendente.
    """
    autos = obtener_autos_api(sort_by=campo, desc=descendente)
    if not autos:
        # El mensaje ya se mostró en obtener_autos_api
        return
    ordenar_autos(autos, campo, descendente)


def estadisticas_api():
    """Muestra estadísticas de autos obtenidos desde la API."""
    autos = obtener_autos_api()
    if not autos:
        # El mensaje ya se mostró en obtener_autos_api
        return
    mostrar_estadisticas(autos)


def agregar_auto_api():
    """Agrega un auto nuevo usando la API."""
    print("\n--- Agregar nuevo auto (API) ---")
    marca = input("Marca del auto: ").strip()
    while marca == "":
        marca = input("La marca no puede estar vacía. Ingresá nuevamente: ").strip()

    modelo = input("Modelo del auto: ").strip()
    while modelo == "":
        modelo = input("El modelo no puede estar vacío. Ingresá nuevamente: ").strip()

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

    try:
        auto_api = api_client.crear_auto(
            marca=marca,
            modelo=modelo,
            año=año,
            tipo_combustible=tipo_combustible,
            transmision=transmision,
        )
        print(f"Auto '{marca} {modelo}' creado correctamente en el servidor.")
    except Exception as e:
        print(f"Error al crear el auto: {e}")


def editar_auto_api():
    """Edita un auto usando la API."""
    print("\n--- Editar auto (API) ---")
    busqueda = input("Ingresá la marca o modelo del auto que querés editar: ").strip()
    if not busqueda:
        print("Búsqueda vacía, cancelado.")
        return

    autos = obtener_autos_api(q=busqueda)
    busqueda_norm = normalizar(busqueda)
    resultados = [
        a for a in autos
        if busqueda_norm in normalizar(a.get("Marca", "")) or busqueda_norm in normalizar(a.get("Modelo", ""))
    ]

    if not resultados:
        print(f" No se encontró ningún auto que contenga '{busqueda}'.")
        return

    print(f"\nSe encontraron {len(resultados)} auto(s):")
    for i, a in enumerate(resultados, 1):
        print(
            f"{i}. {a.get('Marca', '')} {a.get('Modelo', '')} | "
            f"Año: {a.get('Año', '')} | "
            f"Combustible: {a.get('TipoCombustible', '')} | "
            f"Transmisión: {a.get('Transmisión', '')}"
        )

    try:
        indice = int(input("Elegí el número del auto que querés editar: ")) - 1
        if indice < 0 or indice >= len(resultados):
            print(" Número inválido.")
            return

        auto = resultados[indice]

        print(f"\nEditando: {auto.get('Marca', '')} {auto.get('Modelo', '')}")
        print("(Presiona Enter para mantener el valor actual)")

        cambios = {}

        nuevo_modelo = input(f"Nuevo modelo [{auto.get('Modelo', '')}]: ").strip()
        if nuevo_modelo:
            cambios["Modelo"] = nuevo_modelo

        nuevo_combustible = input(f"Nuevo tipo de combustible [{auto.get('TipoCombustible', '')}]: ").strip()
        if nuevo_combustible:
            cambios["TipoCombustible"] = nuevo_combustible

        nueva_transmision = input(f"Nueva transmisión [{auto.get('Transmisión', '')}]: ").strip()
        if nueva_transmision:
            cambios["Transmisión"] = nueva_transmision

        try:
            nuevo_año = input(f"Nuevo año [{auto.get('Año', '')}]: ").strip()
            if nuevo_año:
                año_int = int(nuevo_año)
                if 1900 <= año_int <= 2100:
                    cambios["Año"] = año_int
                else:
                    print("Año inválido. Se mantiene el valor anterior.")
        except ValueError:
            print("Año inválido. Se mantiene el valor anterior.")

        nueva_marca = input(f"Nueva marca [{auto.get('Marca', '')}]: ").strip()
        if nueva_marca:
            cambios["Marca"] = nueva_marca

        if not cambios:
            print("No se realizaron cambios.")
            return

        # Buscar el ID en la API
        auto_id = auto.get("id")
        if not auto_id:
            print("No se pudo determinar el ID del auto en el servidor.")
            return

        try:
            api_client.actualizar_auto_parcial(auto_id, cambios)
            print(f"Datos actualizados para {auto.get('Marca', '')} {auto.get('Modelo', '')}.")
        except Exception as e:
            print(f"Error al actualizar: {e}")

    except ValueError:
        print("Entrada inválida.")


def borrar_auto_api() -> None:
    """Borra un auto usando la API por ID o por marca/modelo."""
    print("\n--- Borrar auto (API) ---")
    modo = input("¿Buscar por (1) marca/modelo o (2) id? : ").strip() or "1"

    if modo == "2":
        try:
            cid = int(input("ID: ").strip())
        except ValueError:
            print("ID inválido.")
            return

        confirma = input(f"¿Confirmás borrar id={cid}? (s/n): ").strip().lower() == "s"
        if not confirma:
            print("Cancelado.")
            return

        try:
            api_client.eliminar_auto(cid)
            print(f"Borrado id={cid} en el servidor.")
        except Exception as e:
            print(f"Error al borrar: {e}")
        return

    # Borrado por marca/modelo
    busqueda = input("Ingresá la marca o modelo (o parte): ").strip()
    if not busqueda:
        print("Búsqueda vacía, cancelado.")
        return

    autos = obtener_autos_api(q=busqueda)
    if not autos:
        print(f"No se encontró ningún auto que contenga '{busqueda}'.")
        return

    mostrar_autos(autos)

    try:
        idx = int(input("Elegí el número del auto a borrar (1..n): ").strip()) - 1
        if idx < 0 or idx >= len(autos):
            print("Número inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    elegido = autos[idx]
    auto_id = elegido.get("id")
    
    if not auto_id:
        print("No se pudo determinar el ID en el servidor.")
        return

    confirma = (
        input(
            f"¿Confirmás borrar '{elegido.get('Marca', '')} {elegido.get('Modelo', '')}' (id={auto_id})? (s/n): "
        )
        .strip()
        .lower()
        == "s"
    )
    if not confirma:
        print("Cancelado.")
        return

    try:
        api_client.eliminar_auto(auto_id)
        print(f"'{elegido.get('Marca', '')} {elegido.get('Modelo', '')}' borrado correctamente (API).")
    except Exception as e:
        print(f"Error al borrar: {e}")
