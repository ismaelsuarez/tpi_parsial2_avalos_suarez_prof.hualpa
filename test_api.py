"""Script de prueba para verificar la conexión con la API de autos."""

import sys
import os

# Configurar paths
script_path = os.path.abspath(__file__)
project_root = os.path.dirname(script_path)
src_dir = os.path.join(project_root, 'src')

if project_root not in sys.path:
    sys.path.append(project_root)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from function import api_client
from function.api_mode import obtener_autos_api

print("=" * 60)
print("TEST DE CONEXIÓN CON LA API")
print("=" * 60)

# 1. Verificar estado del servidor
print("\n1. Verificando estado del servidor...")
try:
    estado = api_client.estado_servidor()
    print(f"✅ Servidor conectado: {estado}")
except Exception as e:
    print(f"❌ Error al conectar: {e}")
    sys.exit(1)

# 2. Obtener datos crudos de la API
print("\n2. Obteniendo datos crudos de la API...")
try:
    datos_crudos = api_client.listar_autos()
    print(f"✅ Datos obtenidos. Tipo: {type(datos_crudos)}")
    print(f"   Cantidad de items: {len(datos_crudos) if isinstance(datos_crudos, list) else 'N/A'}")
    
    if isinstance(datos_crudos, list) and len(datos_crudos) > 0:
        print(f"\n   Primer item crudo (muestra):")
        print(f"   {datos_crudos[0]}")
    else:
        print("   ⚠️ La API devolvió una lista vacía o un tipo inesperado")
except Exception as e:
    print(f"❌ Error al obtener datos: {e}")
    import traceback
    traceback.print_exc()

# 3. Probar obtención de autos
print("\n3. Probando obtención de autos...")
try:
    autos_obtenidos = obtener_autos_api()
    print(f"✅ Obtención exitosa. Autos obtenidos: {len(autos_obtenidos)}")
    
    if len(autos_obtenidos) > 0:
        print(f"\n   Primer auto obtenido (muestra):")
        auto = autos_obtenidos[0]
        print(f"   Marca: {auto.get('Marca')}")
        print(f"   Modelo: {auto.get('Modelo')}")
        print(f"   Año: {auto.get('Año')}")
        print(f"   TipoCombustible: {auto.get('TipoCombustible')}")
        print(f"   Transmisión: {auto.get('Transmisión')}")
    else:
        print("   ⚠️ No se obtuvieron autos")
except Exception as e:
    print(f"❌ Error al obtener autos: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("FIN DEL TEST")
print("=" * 60)
