"""
Módulo de almacenamiento y persistencia para Tribuna Global.
Responsable de la lectura y escritura atómica en archivos JSON,
así como de las consultas y validaciones de estructura.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Definición de rutas base relativas a la ubicación de este archivo.
# Soporta tanto el catálogo de figuras políticas como de futbolistas para máxima versatilidad.
BASE_DIR = Path(__file__).resolve().parent
RUTA_POLITICOS = BASE_DIR / "datos" / "politicos.json"
RUTA_JUGADORES = BASE_DIR / "datos" / "jugadores.json"
RUTA_OPINIONES = BASE_DIR / "datos" / "opiniones.json"
VERSION_PROMPT = "1.0"


def cargar_jugadores(ruta: Optional[Path | str] = None) -> List[Dict[str, str]]:
    """
    Carga y valida el catálogo de figuras públicas (políticos o futbolistas) desde el archivo JSON.
    
    Verificaciones:
    - Que el archivo exista y sea un JSON sintácticamente válido.
    - Que contenga la clave 'politicos' o 'jugadores'.
    - Que no existan identificadores ('id') duplicados en el catálogo.
    
    Retorna:
        Lista de diccionarios con la información de cada figura.
    """
    if ruta:
        ruta_archivo = Path(ruta)
    else:
        # Priorizar el catálogo de políticos si existe, de lo contrario usar jugadores
        ruta_archivo = RUTA_POLITICOS if RUTA_POLITICOS.exists() else RUTA_JUGADORES

    if not ruta_archivo.exists():
        raise FileNotFoundError(f"No se encontró el catálogo en: {ruta_archivo}")

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"El archivo {ruta_archivo} no contiene un JSON válido: {e}")

    # Soporte para ambas claves de catálogo: 'politicos' o 'jugadores'
    clave_catalogo = "politicos" if "politicos" in data else "jugadores"

    if not isinstance(data, dict) or clave_catalogo not in data:
        raise ValueError(f"El catálogo debe contener un objeto con la clave '{clave_catalogo}'.")

    figuras = data[clave_catalogo]
    if not isinstance(figuras, list):
        raise ValueError(f"La clave '{clave_catalogo}' debe ser una lista.")

    # Validación de identificadores únicos
    ids_vistos = set()
    for j in figuras:
        if not isinstance(j, dict) or "id" not in j or "nombre" not in j:
            raise ValueError(f"Elemento con estructura inválida encontrado: {j}")
        
        j_id = j["id"]
        if j_id in ids_vistos:
            raise ValueError(f"Identificador duplicado detectado: '{j_id}'")
        ids_vistos.add(j_id)

    return figuras


# Alias explícito para máxima claridad en el código
cargar_politicos = cargar_jugadores


def cargar_opiniones(ruta: Optional[Path | str] = None) -> Dict[str, Any]:
    """
    Carga el diccionario persistente de opiniones desde el archivo JSON.
    
    Reglas de negocio:
    1. Si el archivo no existe, se inicializa automáticamente la estructura base:
       {"version": 1, "opiniones": []}.
    2. Si el archivo existe pero está corrupto (JSON inválido) o tiene un esquema
       inesperado, se lanza una excepción y se CONSERVA el archivo (nunca se sobreescribe
       silenciosamente con una lista vacía para no perder información).
    
    Retorna:
        Diccionario con la estructura de opiniones persistidas.
    """
    ruta_archivo = Path(ruta) if ruta else RUTA_OPINIONES

    # Si no existe, inicializamos el archivo de forma limpia
    if not ruta_archivo.exists():
        ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        estructura_inicial = {"version": 1, "opiniones": []}
        guardar_diccionario_atomico(ruta_archivo, estructura_inicial)
        return estructura_inicial

    # Si existe, lo leemos cuidadosamente
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        # ¡IMPORTANTE! No sobreescribir el archivo corrupto. Levantamos error para proteger los datos.
        raise ValueError(
            f"El archivo de opiniones en {ruta_archivo} está dañado o tiene formato inválido. "
            f"Se ha conservado intacto para evitar pérdida de datos. Detalle: {e}"
        )

    # Validar el esquema básico
    if not isinstance(data, dict) or "opiniones" not in data or not isinstance(data["opiniones"], list):
        raise ValueError(
            f"El archivo {ruta_archivo} no cumple con el esquema esperado ('version' y lista 'opiniones')."
        )

    return data


def crear_registro(
    jugador: Dict[str, str],
    texto: str,
    analisis: Any,
    modelo: str
) -> Dict[str, Any]:
    """
    Construye el registro estructurado de una opinión analizada, incorporando
    metadatos del sistema (UUID único, timestamp UTC, versión del prompt, etc.).
    
    Parámetros:
        jugador: Diccionario con 'id' y 'nombre' del futbolista.
        texto: Opinión original del aficionado (limpia).
        analisis: Objeto de análisis (debe poseer atributos o claves 'sentimiento' y 'razon').
        modelo: Nombre del modelo LLM utilizado.
        
    Retorna:
        Diccionario listo para ser persistido en disco.
    """
    # Soporta tanto objetos Pydantic (analisis.sentimiento) como diccionarios
    sentimiento = getattr(analisis, "sentimiento", None)
    if sentimiento is None and isinstance(analisis, dict):
        sentimiento = analisis.get("sentimiento")

    razon = getattr(analisis, "razon", None)
    if razon is None and isinstance(analisis, dict):
        razon = analisis.get("razon")

    return {
        "id": str(uuid.uuid4()),
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "jugador_id": jugador["id"],
        "jugador_nombre": jugador["nombre"],
        "opinion_original": texto,
        "sentimiento": sentimiento,
        "razon": razon,
        "modelo": modelo,
        "version_prompt": VERSION_PROMPT
    }


def guardar_diccionario_atomico(ruta_archivo: Path, data: Dict[str, Any]) -> None:
    """
    Escribe un diccionario en un archivo JSON utilizando una técnica de escritura atómica:
    1. Escribe primero en un archivo temporal (.tmp) en el mismo directorio.
    2. Utiliza os.replace para reemplazar el archivo de destino de golpe.
    
    Esto evita que el archivo final quede a medias o corrupto si la aplicación
    se interrumpe o se queda sin energía en medio de la escritura.
    """
    ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
    # El archivo temporal se crea en la misma carpeta para que estén en el mismo volumen de disco
    ruta_temporal = ruta_archivo.with_suffix(".tmp")

    try:
        with open(ruta_temporal, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # Reemplazo atómico garantizado por el sistema operativo
        os.replace(ruta_temporal, ruta_archivo)
    except Exception as e:
        # Si algo falla antes del reemplazo, limpiamos el archivo temporal si existe
        if ruta_temporal.exists():
            try:
                ruta_temporal.unlink()
            except OSError:
                pass
        raise IOError(f"Error durante la escritura atómica en {ruta_archivo}: {e}")


def guardar_opinion(ruta: Optional[Path | str], registro: Dict[str, Any]) -> None:
    """
    Añade un nuevo registro de opinión al archivo JSON persistente sin perder
    los registros previos.
    
    Verifica además que no se inserte un registro con un ID ya existente
    para evitar duplicaciones accidentales durante reintentos.
    """
    ruta_archivo = Path(ruta) if ruta else RUTA_OPINIONES
    data = cargar_opiniones(ruta_archivo)

    # Verificar si el ID ya existe para evitar duplicación por reejecución
    ids_existentes = {op["id"] for op in data["opiniones"] if "id" in op}
    if registro["id"] in ids_existentes:
        # El registro ya fue persistido previamente, no se duplica
        return

    data["opiniones"].append(registro)
    guardar_diccionario_atomico(ruta_archivo, data)


def consultar_opiniones(
    registros: List[Dict[str, Any]],
    jugador_id: Optional[str] = None,
    sentimiento: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filtra los registros de opiniones en memoria sin realizar ninguna consulta al LLM.
    
    Parámetros:
        registros: Lista de opiniones cargadas.
        jugador_id: ID del jugador para filtrar (o None / 'todos' para no filtrar).
        sentimiento: Categoría de sentimiento (o None / 'todos' para no filtrar).
        
    Retorna:
        Lista de registros que cumplen con todos los criterios de filtrado.
    """
    resultado = []
    
    filtro_jugador = jugador_id.lower().strip() if jugador_id else "todos"
    filtro_sentimiento = sentimiento.lower().strip() if sentimiento else "todos"

    for r in registros:
        # Filtro de jugador
        if filtro_jugador not in ("todos", "all", ""):
            if r.get("jugador_id", "").lower() != filtro_jugador:
                continue

        # Filtro de sentimiento
        if filtro_sentimiento not in ("todos", "all", ""):
            if str(r.get("sentimiento", "")).lower() != filtro_sentimiento:
                continue

        resultado.append(r)

    return resultado
