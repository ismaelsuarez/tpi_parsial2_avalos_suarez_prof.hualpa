# TPI Programación 1 — Gestión de Autos (Python)

Aplicación de **consola** para consultar y administrar datos de autos desde un **CSV local** o una **API REST** remota. Permite **búsquedas**, **filtros**, **ordenamientos**, **estadísticas** y **CRUD** básico.

> Proyecto orientado a cursado inicial (UTN FRM). Código y mensajes en **español**, con funciones sencillas y docstrings estilo Google.

---

## Tabla de contenidos
- [Características](#características)
- [Modos de operación](#modos-de-operación)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración rápida](#configuración-rápida)
- [Ejecución](#ejecución)
- [Menú principal](#menú-principal)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Flujo de datos](#flujo-de-datos)
- [Guía para desarrolladores](#guía-para-desarrolladores)
- [Solución de problemas](#solución-de-problemas)
- [Créditos](#créditos)

---

## Características
- **Fuente de datos dual**:
  - **Local**: `src/db/autos.csv` (lectura/escritura)
  - **API**: servidor FastAPI (HTTP GET/POST/PATCH/DELETE) en `http://149.50.150.15:8010`
- **Operaciones**: 
  - Buscar por marca o modelo
  - Filtrar por tipo de combustible
  - Filtrar por rango de año
  - Filtrar por transmisión
  - Ordenar por cualquier campo (Marca, Modelo, Año, TipoCombustible, Transmisión)
  - Estadísticas (auto más antiguo/nuevo, promedio de años, conteos por marca/combustible/transmisión)
- **CRUD completo**: agregar, editar y borrar autos (en local o API).
- **Compatibilidad**: mensajes en español y funciones con **nombres en español** (por ejemplo, `estado_servidor`, `buscar_auto`, `agregar_auto`, `listar_autos`).
- **Docstrings**: estilo Google en todos los módulos (mantenibles y legibles).

---

## Modos de operación
- **Local (CSV)**: trabaja con `src/db/autos.csv`. Si no existe, el sistema lo **crea** automáticamente con el encabezado correspondiente.
- **API**: consume un servidor FastAPI en `http://149.50.150.15:8010` usando el endpoint `/autos`. La API utiliza directamente el esquema de autos con los campos: `Marca`, `Modelo`, `Año`, `TipoCombustible`, `Transmisión`.

---

## Requisitos
- **Python** \>= 3.10 (probado en 3.13)
- **Sistema operativo**: Windows / Linux / macOS
- **Dependencias** (modo API): `requests`

**Instalación rápida de dependencias**
```bash
# Windows (PowerShell/CMD)
py -3.13 -m pip install --upgrade pip
py -3.13 -m pip install requests

# Linux / macOS
python3 -m pip install --upgrade pip
python3 -m pip install requests
```

Opcional: `requirements.txt`
```text
requests>=2.32.0
```

> Recomendado: crear un **entorno virtual** (venv) antes de instalar dependencias.

---

## Instalación
**Clonar el repositorio**
```bash
git clone https://github.com/pabloavalos25/TPI-prog1-C4-SUAREZ----AVALOS
cd TPI-prog1-C4-SUAREZ----AVALOS
```

**O descargar ZIP**
1. Abrí el repo en GitHub
2. `Code` → `Download ZIP`
3. Descomprimí la carpeta y abrila en tu editor

---

## Configuración rápida
- **URL de la API**: se define en `src/function/api_client.py` como `BASE_URL` (sin barra final):
  ```python
  BASE_URL = "http://149.50.150.15:8010"
  ```
- **CSV inicial**: si `src/db/autos.csv` no existe, se crea automáticamente con encabezado:
  ```csv
  Marca,Modelo,Año,TipoCombustible,Transmisión
  ```
  Codificación: **UTF-8 con BOM** (para compatibilidad en Windows).

---

## Ejecución
**Windows**
```bash
py app/main.py
# Alternativa
python app/main.py
```
**Linux / macOS**
```bash
python3 app/main.py
```
Al inicio, el sistema:
1. Verifica/crea `src/db/autos.csv` (mueve el archivo si estaba en otra carpeta del proyecto).
2. Solicita el **modo**:
   ```text
   ****Seleccione el servidor****
   1. CSV local
   2. CSV API
   3. Salir
   ```
3. Si elegís API, verifica `/health` con `estado_servidor()` en `http://149.50.150.15:8010`.

---

## Menú principal
```text
**********GESTIÓN DE AUTOS**********
1.  Buscar auto por marca o modelo
2.  Filtrar por tipo de combustible
3.  Filtrar por rango de año
4.  Filtrar por transmisión
5.  Ordenar autos
6.  Mostrar estadisticas
7.  Agregar un auto
8.  Editar un auto
9.  Borrar auto
10. Cambiar modo de servidor
11. Salir
```

**Notas de uso**
- En **Local**, las modificaciones persisten en `src/db/autos.csv`.
- En **API**, se invocan los endpoints remotos:
  - `GET /autos` - Listar todos los autos (con filtros opcionales)
  - `GET /autos/{id}` - Obtener un auto por ID
  - `POST /autos` - Crear un nuevo auto
  - `PATCH /autos/{id}` - Actualizar parcialmente un auto
  - `DELETE /autos/{id}` - Eliminar un auto
- Los campos usados son directamente: `Marca`, `Modelo`, `Año`, `TipoCombustible`, `Transmisión` (sin mapeos ni conversiones).

---

## Estructura de carpetas
```text
app/
  └─ main.py               # Menú y selección de fuente (Local/API)
src/
  ├─ db/
  │   └─ autos.csv         # Base de datos local (CSV)
  ├─ doc/
  │   └─ TPI-Programacion1_2025_Comision4_Grupo6_parcial2.pdf
  └─ function/
      ├─ api_client.py     # Cliente HTTP (estado_servidor, listar_autos, crear_auto, etc.)
      ├─ api_mode.py       # Lógica de modo API: funciones que interactúan con la API
      ├─ data_load.py      # Altas, ediciones y borrados en modo local (CSV)
      ├─ init.py           # Ubica/mueve/crea autos.csv al iniciar
      ├─ shearch.py        # Búsquedas y filtros (local)
      ├─ statistics.py     # Estadísticas generales
      ├─ tools.py          # Utilidades: normalizar, leer/escribir CSV, menús y mensajes
      └─ view.py           # Presentación: listado, ordenar, pedir rangos
README.md
```

---

## Flujo de datos

### Modo Local
1. **Lectura**: `tools.leer_csv()` → lee `src/db/autos.csv` y retorna lista de dicts con estructura:
   ```python
   {
       "Marca": "Toyota",
       "Modelo": "Corolla",
       "Año": 2020,
       "TipoCombustible": "Nafta",
       "Transmisión": "Automática"
   }
   ```
2. **CRUD en memoria**: funciones en `data_load.py` (agregar, editar, borrar)
3. **Persistencia**: `tools.escribir_csv()` → guarda cambios en `src/db/autos.csv`

### Modo API
1. **Cliente HTTP**: `api_client.py` realiza peticiones al servidor:
   - `estado_servidor()` → `GET /health`
   - `listar_autos(q, tipo_combustible, ordenar_por, descendente)` → `GET /autos`
   - `obtener_auto(id)` → `GET /autos/{id}`
   - `crear_auto(marca, modelo, año, tipo_combustible, transmision)` → `POST /autos`
   - `actualizar_auto_parcial(id, cambios)` → `PATCH /autos/{id}`
   - `eliminar_auto(id)` → `DELETE /autos/{id}`
2. **Lógica de API**: `api_mode.py` contiene funciones que usan `api_client` y reutilizan funciones de `view.py`, `shearch.py`, `statistics.py` con los datos obtenidos de la API
3. **Esquema directo**: La API retorna y acepta datos con los campos reales del CSV (`Marca`, `Modelo`, `Año`, `TipoCombustible`, `Transmisión`) sin conversiones ni mapeos

---

## Guía para desarrolladores

### Estilo y documentación
- Código y nombres en **español**.
- **Docstrings** estilo Google (módulos, funciones, clases, métodos). Ejemplo:
  ```python
  def listar_autos(
      q: str | None = None,
      tipo_combustible: str | None = None,
      ordenar_por: str | None = None,
      descendente: bool = False,
  ) -> list[dict]:
      """Lista autos con filtros y orden opcional.

      Args:
          q (str | None): Texto para buscar por marca o modelo.
          tipo_combustible (str | None): Filtro por tipo de combustible.
          ordenar_por (str | None): Campo de orden (ej.: 'Marca', 'Modelo', 'Año').
          descendente (bool): Si True, orden descendente.

      Returns:
          list[dict]: Lista de autos con estructura: Marca, Modelo, Año, TipoCombustible, Transmisión.
      """
  ```

### Estructura de datos
- Los autos se representan como diccionarios con las siguientes claves:
  - `Marca` (str): Marca del vehículo (ej: "Toyota", "Ford")
  - `Modelo` (str): Modelo del vehículo (ej: "Corolla", "Focus")
  - `Año` (int): Año de fabricación (ej: 2020, 2018)
  - `TipoCombustible` (str): Tipo de combustible (ej: "Nafta", "Diesel", "Eléctrico")
  - `Transmisión` (str): Tipo de transmisión (ej: "Manual", "Automática", "CVT")


---

## Solución de problemas

- **No inicia y aparece un ImportError genérico**
  - Verificá que `src/` o la raíz que contiene `function/` estén en `sys.path`.
  - `main.py` ya incluye lógica para ubicar `function`. Si moviste carpetas, revisá las rutas.

- **Error 404 al consultar la API**
  - Verificá que la URL de la API sea correcta en `src/function/api_client.py`.
  - Verificá que el servidor esté corriendo y accesible: `curl http://149.50.150.15:8010/health`
  - Verificá que el endpoint `/autos` exista en el servidor.

- **Python < 3.10**
  - Evitá anotaciones con `|` (Union). Usá `from typing import Union, Optional`.

- **`requests` no instalado (modo API)**
  - Instalalo con `py -3.13 -m pip install requests` (Windows) o `python3 -m pip install requests` (Linux/macOS).

- **CSV vacío o con filas inválidas**
  - El sistema omite filas inválidas e informa cuántas ignoró. Podés abrir el CSV y completar manualmente.

- **Acentos o caracteres raros en consola**
  - Usá PowerShell o Windows Terminal con UTF-8 (o una terminal moderna en Linux/macOS).

- **La API no devuelve datos**
  - Verificá que el servidor tenga datos cargados.
  - Probá el endpoint directamente: `curl http://149.50.150.15:8010/autos`
  - Verificá los logs del servidor si tenés acceso.

---

## Créditos
- **Universidad**: UTN — Facultad Regional Mendoza
- **Carrera**: Tecnicatura Universitaria en Programación
- **Año**: 2025
- **Integrantes**: *Avalos, Pablo* — *Suárez, Ismael*
- **Video Presentación**: 

#   t p i _ p a r s i a l 2 _ a v a l o s _ s u a r e z _ p r o f . h u a l p a  
 