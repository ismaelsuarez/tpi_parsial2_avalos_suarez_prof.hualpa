"""Cliente HTTP sencillo para hablar con el servidor de la API de autos.

Este módulo ofrece funciones básicas para:
- Verificar si el servidor está en línea.
- Listar, buscar, crear, actualizar y eliminar autos desde la API.

Las funciones usan solicitudes HTTP (GET/POST/PATCH/DELETE) con `requests`.
Se busca un código claro y simple, ideal para primer año.
"""

from typing import Optional, List, Dict

try:
    import requests
except ImportError:
    raise SystemExit(
        "*********************😎****************************\n"
        "*          Falta el paquete 'requests'.           *\n"
        "* Tener presente la version de python que tienes  *\n"
        "* Por ejemplo tengo pythob 3.13:                  *\n"
        "*   Windows: py -3.13 -m pip install requests     *\n"
        "*   Linux/Mac: python3 -m pip install requests    *\n"
        "* Es fundamental para que el proyecto funcione    *\n"
        "* Se utiliza para comunicarse con el servidor API *\n"
        "*********************👌***************************"
    )

# URL base del servidor de la API (sin barra final).
BASE_URL = "http://149.50.150.15:8010".rstrip("/")


def _url(ruta: str) -> str:
    """Arma una URL completa a partir de la ruta.

    Args:
        ruta (str): Ruta que comienza con '/' (por ejemplo, '/autos').

    Returns:
        str: URL lista para usar en la petición HTTP.
    """
    return f"{BASE_URL}{ruta}"


def establecer_base_url(url: str) -> None:
    """Cambia la URL base del servidor API.

    Args:
        url (str): Nueva URL base. Se ignora la barra final si existe.
    """
    global BASE_URL
    BASE_URL = (url or "").rstrip("/")


def estado_servidor() -> Dict:
    """Consulta el estado del servidor (endpoint de salud).

    Returns:
        dict: Respuesta JSON con información de estado.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta (4xx/5xx).
    """
    resp = requests.get(_url("/health"), timeout=5)
    resp.raise_for_status()
    return resp.json()


def listar_autos(
    q: Optional[str] = None,
    tipo_combustible: Optional[str] = None,
    ordenar_por: Optional[str] = None,
    descendente: bool = False,
) -> List[Dict]:
    """Lista autos con filtros y orden opcional.

    Args:
        q (str | None): Texto para buscar por marca o modelo.
        tipo_combustible (str | None): Filtro por tipo de combustible.
        ordenar_por (str | None): Campo de orden (ej.: 'Marca', 'Modelo', 'Año').
        descendente (bool): Si True, orden descendente.

    Returns:
        list[dict]: Lista de autos con estructura: Marca, Modelo, Año, TipoCombustible, Transmisión.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta.
    """
    params: Dict[str, str] = {}
    if q:
        params["q"] = q
    if tipo_combustible:
        params["TipoCombustible"] = tipo_combustible
    if ordenar_por:
        params["sort_by"] = ordenar_por
    if descendente:
        params["desc"] = "true"

    resp = requests.get(_url("/autos"), params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def obtener_auto(id_auto: int) -> Dict:
    """Obtiene un auto por su identificador numérico.

    Args:
        id_auto (int): Identificador del auto.

    Returns:
        dict: Datos del auto.

    Raises:
        requests.HTTPError: Si no existe o hay error del servidor.
    """
    resp = requests.get(_url(f"/autos/{id_auto}"), timeout=10)
    resp.raise_for_status()
    return resp.json()


def crear_auto(
    marca: str,
    modelo: str,
    año: int,
    tipo_combustible: str,
    transmision: str,
) -> Dict:
    """Crea un auto nuevo en el servidor.

    Args:
        marca (str): Marca del auto.
        modelo (str): Modelo del auto.
        año (int): Año del auto.
        tipo_combustible (str): Tipo de combustible.
        transmision (str): Tipo de transmisión.

    Returns:
        dict: Auto creado (respuesta del servidor).

    Raises:
        requests.HTTPError: Si la creación falla.
    """
    payload = {
        "Marca": marca,
        "Modelo": modelo,
        "Año": int(año),
        "TipoCombustible": tipo_combustible,
        "Transmisión": transmision,
    }
    resp = requests.post(_url("/autos"), json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def actualizar_auto_parcial(id_auto: int, cambios: Dict) -> Dict:
    """Actualiza parcialmente un auto (solo los campos enviados).

    Args:
        id_auto (int): Identificador del auto a modificar.
        cambios (dict): Campos a actualizar (ej.: {'Modelo': 'Nuevo', 'Año': 2024}).

    Returns:
        dict: Auto actualizado.

    Raises:
        requests.HTTPError: Si la actualización falla.
    """
    resp = requests.patch(_url(f"/autos/{id_auto}"), json=cambios, timeout=10)
    resp.raise_for_status()
    return resp.json()


def eliminar_auto(id_auto: int) -> bool:
    """Elimina un auto por su identificador.

    Args:
        id_auto (int): Identificador del auto.

    Returns:
        bool: True si el servidor aceptó la eliminación.

    Raises:
        requests.HTTPError: Si el servidor devuelve un error.
    """
    resp = requests.delete(_url(f"/autos/{id_auto}"), timeout=10)
    if resp.status_code not in (200, 204):
        resp.raise_for_status()
    return True


def listar_todos(
    ordenar_por: Optional[str] = None,
    descendente: bool = False,
) -> List[Dict]:
    """Devuelve todos los autos con orden opcional.

    Args:
        ordenar_por (str | None): Campo de orden.
        descendente (bool): Si True, orden descendente.

    Returns:
        list[dict]: Lista completa de autos.
    """
    return listar_autos(ordenar_por=ordenar_por, descendente=descendente)


def buscar_por_modelo(modelo: str) -> Optional[Dict]:
    """Busca un auto por modelo (intenta coincidencia exacta primero).

    Si no encuentra coincidencia exacta, devuelve el primer resultado de la lista.

    Args:
        modelo (str): Modelo a buscar.

    Returns:
        dict | None: Auto encontrado o None si no hay resultados.
    """
    if not modelo:
        return None

    candidatos = listar_autos(q=modelo, ordenar_por="Modelo")
    n = (modelo or "").strip().lower()
    for c in candidatos:
        if c.get("Modelo", "").strip().lower() == n:
            return c
    return candidatos[0] if candidatos else None


def crear_desde_dict(auto: Dict) -> Dict:
    """Crea un auto a partir de un diccionario con las claves del CSV.

    Args:
        auto (dict): Debe incluir 'Marca', 'Modelo', 'Año', 'TipoCombustible', 'Transmisión'.

    Returns:
        dict: Auto creado (respuesta del servidor).

    Raises:
        KeyError: Si faltan claves requeridas en el diccionario.
        requests.HTTPError: Si la creación falla.
    """
    return crear_auto(
        marca=auto["Marca"],
        modelo=auto["Modelo"],
        año=int(auto["Año"]),
        tipo_combustible=auto["TipoCombustible"],
        transmision=auto["Transmisión"],
    )
