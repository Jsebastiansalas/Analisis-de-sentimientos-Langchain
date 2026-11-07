"""
API REST con FastAPI para Ágora Colombia / Tribuna Global.
Expone endpoints para consultar el catálogo de figuras políticas,
analizar opiniones con IA en tiempo real y consultar registros persistentes.
"""

import json
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from almacenamiento import (
    cargar_jugadores,
    cargar_opiniones,
    crear_registro,
    guardar_opinion,
    consultar_opiniones,
    corregir_opinion,
    RUTA_OPINIONES
)
from analisis import (
    analizar_opinion,
    validar_texto_opinion,
    DEFAULT_MODEL
)

app = FastAPI(
    title="Ágora Colombia API - Barómetro de Percepción Ciudadana",
    description="API RESTful para análisis de sentimiento estructurado con LangChain y Google Gemini / OpenAI",
    version="2.0.0"
)

# Habilitar CORS para permitir llamadas desde el frontend web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para los requests de la API
class EnvioOpinionRequest(BaseModel):
    politico_id: str = Field(..., description="ID de la figura política (ej. 'p001')")
    opinion: str = Field(..., min_length=5, max_length=1000, description="Texto de la opinión ciudadana")


class CorreccionOpinionRequest(BaseModel):
    nuevo_sentimiento: str = Field(..., description="Nuevo sentimiento ('positivo', 'negativo', 'neutro', 'mixto')")
    justificacion: Optional[str] = Field("", description="Justificación de la reclasificación humana")


@app.get("/api/politicos", summary="Obtener catálogo de figuras políticas")
def obtener_politicos():
    """Retorna la lista de figuras políticas colombianas validadas."""
    try:
        politicos = cargar_jugadores()
        return {"total": len(politicos), "politicos": politicos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar catálogo: {e}")


@app.get("/api/opiniones", summary="Consultar opiniones persistidas con métricas")
def obtener_opiniones(
    politico_id: Optional[str] = Query(None, description="Filtrar por ID de político o 'todos'"),
    sentimiento: Optional[str] = Query(None, description="Filtrar por categoría de sentimiento o 'todos'"),
    q: Optional[str] = Query(None, description="Filtrar por palabra clave en opinión o razón")
):
    """
    Retorna las opiniones filtradas y un resumen estadístico sincronizado.
    Cero llamadas al modelo LLM.
    """
    try:
        data = cargar_opiniones(RUTA_OPINIONES)
        registros = data.get("opiniones", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer base de datos: {e}")

    filtradas = consultar_opiniones(registros, jugador_id=politico_id, sentimiento=sentimiento, texto_busqueda=q)

    # Calcular desglose estadístico
    total = len(filtradas)
    metricas = {
        "total": total,
        "positivo": sum(1 for op in filtradas if op.get("sentimiento") == "positivo"),
        "negativo": sum(1 for op in filtradas if op.get("sentimiento") == "negativo"),
        "neutro": sum(1 for op in filtradas if op.get("sentimiento") == "neutro"),
        "mixto": sum(1 for op in filtradas if op.get("sentimiento") == "mixto"),
    }

    return {
        "metricas": metricas,
        "opiniones": filtradas
    }


@app.post("/api/opiniones", summary="Analizar y registrar una nueva opinión ciudadana")
def registrar_opinion(peticion: EnvioOpinionRequest):
    """
    Valida el texto, realiza inferencia de sentimiento con LangChain y,
    si es pertinente, persiste atómicamente el registro en opiniones.json.
    """
    # 1. Validar longitud
    try:
        texto_limpio = validar_texto_opinion(peticion.opinion)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    # 2. Buscar figura en el catálogo
    catalogo = cargar_jugadores()
    politico_obj = next((p for p in catalogo if p["id"] == peticion.politico_id), None)
    if not politico_obj:
        raise HTTPException(status_code=404, detail=f"Figura política con ID '{peticion.politico_id}' no encontrada.")

    # 3. Analizar con LangChain / LLM
    try:
        analisis = analizar_opinion(
            jugador_nombre=politico_obj["nombre"],
            texto_opinion=texto_limpio
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Fallo en la inferencia con IA: {e}")

    # 4. Guardado condicional según pertinencia
    registro_guardado = None
    if analisis.es_pertinente:
        try:
            registro_guardado = crear_registro(
                jugador=politico_obj,
                texto=texto_limpio,
                analisis=analisis,
                modelo=DEFAULT_MODEL
            )
            guardar_opinion(RUTA_OPINIONES, registro_guardado)
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error de almacenamiento atómico: {err}")

    return {
        "es_pertinente": analisis.es_pertinente,
        "sentimiento": analisis.sentimiento,
        "razon": analisis.razon,
        "guardado": analisis.es_pertinente,
        "registro": registro_guardado
    }


@app.post("/api/opiniones/{opinion_id}/corregir", summary="Reclasificación manual (Human-in-the-Loop)")
def corregir_opinion_endpoint(opinion_id: str, peticion: CorreccionOpinionRequest):
    """
    Permite a un auditor humano corregir la etiqueta de sentimiento asignada por la IA,
    preservando el valor original y cumpliendo con los desafíos de ampliación (Sección 12).
    """
    validos = {"positivo", "negativo", "neutro", "mixto"}
    if peticion.nuevo_sentimiento.lower() not in validos:
        raise HTTPException(status_code=400, detail=f"Sentimiento inválido. Debe ser uno de {validos}")

    try:
        modificado = corregir_opinion(
            ruta=RUTA_OPINIONES,
            opinion_id=opinion_id,
            nuevo_sentimiento=peticion.nuevo_sentimiento.lower(),
            justificacion=peticion.justificacion or ""
        )
        return {"status": "ok", "registro": modificado}
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=str(ke))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar corrección: {e}")


@app.get("/api/exportar", summary="Descargar opiniones filtradas en formato JSON")
def exportar_opiniones(
    politico_id: Optional[str] = Query(None),
    sentimiento: Optional[str] = Query(None)
):
    """Devuelve un archivo JSON descargable con las opiniones filtradas."""
    try:
        data = cargar_opiniones(RUTA_OPINIONES)
        registros = data.get("opiniones", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    filtradas = consultar_opiniones(registros, jugador_id=politico_id, sentimiento=sentimiento)
    json_bytes = json.dumps(filtradas, ensure_ascii=False, indent=2).encode("utf-8")

    return Response(
        content=json_bytes,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=agora_colombia_opiniones.json"}
    )


# Servir frontend estático si existe la carpeta 'static'
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
