"""
Tribuna Global - Aplicación de Percepción de Futbolistas
Construida con Streamlit, LangChain y Salida Estructurada con Pydantic.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from almacenamiento import (
    cargar_jugadores,
    cargar_opiniones,
    crear_registro,
    guardar_opinion,
    consultar_opiniones,
    RUTA_OPINIONES
)
from analisis import (
    analizar_opinion,
    validar_texto_opinion,
    MIN_CARACTERES,
    MAX_CARACTERES,
    DEFAULT_MODEL
)

# Cargar variables de entorno locales
load_dotenv()

# Configuración visual de la página
st.set_page_config(
    page_title="Tribuna Global - Chatbot de Futbolistas",
    page_icon="⚽",
    layout="wide"
)

# Constantes de estilos para sentimientos
BADGES_SENTIMIENTO = {
    "positivo": "🟢 Positivo",
    "negativo": "🔴 Negativo",
    "neutro": "⚪ Neutro",
    "mixto": "🟡 Mixto"
}

# ---------------------------------------------------------
# 1. CARGA INICIAL DE DATOS
# ---------------------------------------------------------
try:
    catalogo_jugadores = cargar_jugadores()
except Exception as e:
    st.error(f"❌ Error crítico al cargar el catálogo de futbolistas: {e}")
    st.stop()

# ---------------------------------------------------------
# 2. BARRA LATERAL (Configuración y Selección de Jugador)
# ---------------------------------------------------------
with st.sidebar:
    st.title("⚽ Tribuna Global")
    st.markdown("---")
    
    st.header("👤 Selección de Futbolista")
    
    # Formateo de las opciones: "Nombre (País)"
    opciones_jugador = {
        f"{j['nombre']} ({j['pais']})": j for j in catalogo_jugadores
    }
    
    seleccion_etiqueta = st.selectbox(
        "Elige el futbolista sobre el que opinarás:",
        options=list(opciones_jugador.keys()),
        help="La opinión que envíes quedará asociada permanentemente a este futbolista."
    )
    jugador_seleccionado = opciones_jugador[seleccion_etiqueta]
    
    # Información del jugador actual
    st.caption(f"**ID Interno:** `{jugador_seleccionado['id']}`")
    st.caption(f"**Nacionalidad:** {jugador_seleccionado['pais']}")
    
    st.markdown("---")
    st.header("⚙️ Configuración del Sistema")
    
    # Manejo de API Key: prioriza .env, permite input si no está configurada
    env_api_key = os.getenv("OPENAI_API_KEY", "")
    if env_api_key and env_api_key != "clave_configurada_localmente":
        api_key_activa = env_api_key
        st.success("🔑 API Key detectada desde `.env`")
    else:
        api_key_activa = st.text_input(
            "OpenAI API Key:",
            type="password",
            help="Ingresa tu clave de OpenAI si no la has colocado en el archivo .env"
        )
    
    modelo_seleccionado = st.selectbox(
        "Modelo de IA:",
        options=[DEFAULT_MODEL, "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0
    )
    
    st.caption("ℹ️ **Temperatura:** 0.0 (Fija para garantizar determinismo y rigor analítico).")
    
    st.markdown("---")
    # Botón para limpiar únicamente la sesión visual de chat
    if st.button("🗑️ Nueva conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.toast("Conversación reiniciada. Los registros en disco se conservan intactos.")
        st.rerun()

# ---------------------------------------------------------
# 3. GESTIÓN DEL ESTADO DE SESIÓN (st.session_state)
# ---------------------------------------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# ---------------------------------------------------------
# 4. PESTAÑAS PRINCIPALES DE LA APLICACIÓN
# ---------------------------------------------------------
tab_opinar, tab_consultar = st.tabs(["💬 Emitir opinión", "📊 Consultar opiniones"])

# =========================================================
# SECCIÓN 1: EMITIR OPINIÓN (Chatbot)
# =========================================================
with tab_opinar:
    st.subheader(f"Opinando sobre: **{jugador_seleccionado['nombre']}** ({jugador_seleccionado['pais']})")
    st.markdown(
        "Escribe tu opinión objetiva, crítica o elogio sobre este futbolista (entre 5 y 1000 caracteres). "
        "El sistema analizará el sentimiento con IA y lo guardará en el registro persistente."
    )
    
    # Renderizar historial visual de la sesión actual
    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(f"**[{msg['jugador_nombre']}]**: {msg['content']}")
            else:
                if msg.get("es_pertinente", True):
                    sentimiento = msg.get("sentimiento", "neutro")
                    badge = BADGES_SENTIMIENTO.get(sentimiento, sentimiento)
                    st.markdown(f"**Clasificación:** {badge}")
                    st.markdown(f"**Justificación:** {msg.get('razon', '')}")
                    if msg.get("guardado", False):
                        st.caption("💾 *Registro guardado exitosamente en `opiniones.json`*")
                else:
                    st.warning(f"⚠️ **Opinión no pertinente:** {msg.get('razon', '')}")
                    st.caption("ℹ️ *Este mensaje no fue registrado en el archivo persistente.*")

    # Entrada de texto mediante st.chat_input
    texto_usuario = st.chat_input(f"Escribe tu opinión sobre {jugador_seleccionado['nombre']}...")

    if texto_usuario:
        # 1. Congelar la selección del jugador en el instante exacto del envío
        jugador_envio = {
            "id": jugador_seleccionado["id"],
            "nombre": jugador_seleccionado["nombre"],
            "pais": jugador_seleccionado["pais"]
        }
        
        # 2. Validación de entrada (longitud entre 5 y 1000)
        try:
            texto_limpio = validar_texto_opinion(texto_usuario)
        except ValueError as ve:
            st.warning(f"⚠️ {ve}")
            st.stop()
            
        # 3. Mostrar inmediatamente el mensaje del usuario en pantalla y guardarlo en el estado de sesión
        st.session_state.mensajes.append({
            "role": "user",
            "content": texto_limpio,
            "jugador_id": jugador_envio["id"],
            "jugador_nombre": jugador_envio["nombre"]
        })
        
        with st.chat_message("user"):
            st.markdown(f"**[{jugador_envio['nombre']}]**: {texto_limpio}")
            
        # 4. Procesamiento con LangChain y LLM
        with st.chat_message("assistant"):
            with st.spinner("Analizando sentimiento de forma objetiva..."):
                try:
                    analisis = analizar_opinion(
                        jugador_nombre=jugador_envio["nombre"],
                        texto_opinion=texto_limpio,
                        modelo=modelo_seleccionado,
                        api_key=api_key_activa
                    )
                except ValueError as ve:
                    st.error(f"❌ Error de configuración: {ve}")
                    st.stop()
                except Exception as e:
                    # Ante fallo de API o red, mostrar error claro y no inventar neutro
                    st.error(f"❌ No se pudo completar el análisis: {e}")
                    st.info("💡 Tu opinión se mantiene en pantalla para que no pierdas lo que escribiste.")
                    st.stop()

            # 5. Evaluación de pertinencia y guardado condicional
            if not analisis.es_pertinente:
                st.warning(f"⚠️ **Opinión no pertinente:** {analisis.razon}")
                st.caption("ℹ️ *El comentario no guarda relación con el futbolista. No se ha guardado en disco.*")
                
                st.session_state.mensajes.append({
                    "role": "assistant",
                    "content": analisis.razon,
                    "es_pertinente": False,
                    "sentimiento": None,
                    "razon": analisis.razon,
                    "guardado": False
                })
            else:
                # La opinión es pertinente: mostramos la clasificación
                badge = BADGES_SENTIMIENTO.get(analisis.sentimiento, analisis.sentimiento)
                st.markdown(f"**Clasificación:** {badge}")
                st.markdown(f"**Justificación:** {analisis.razon}")
                
                # Crear y persistir el registro en opiniones.json de forma atómica
                try:
                    registro = crear_registro(
                        jugador=jugador_envio,
                        texto=texto_limpio,
                        analisis=analisis,
                        modelo=modelo_seleccionado
                    )
                    guardar_opinion(RUTA_OPINIONES, registro)
                    st.success("✅ Opinión registrada y guardada exitosamente en el sistema.")
                    
                    st.session_state.mensajes.append({
                        "role": "assistant",
                        "content": analisis.razon,
                        "es_pertinente": True,
                        "sentimiento": analisis.sentimiento,
                        "razon": analisis.razon,
                        "guardado": True
                    })
                except Exception as err_escritura:
                    st.error(f"❌ Falló el almacenamiento del registro: {err_escritura}")


# =========================================================
# SECCIÓN 2: CONSULTAR OPINIONES (Auditoría y Filtros)
# =========================================================
with tab_consultar:
    st.subheader("📊 Registros Persistidos en Disco")
    st.markdown("Esta sección lee directamente desde `opiniones.json` **sin consumir llamadas al modelo de IA**.")
    
    try:
        datos_guardados = cargar_opiniones(RUTA_OPINIONES)
        opiniones_existentes = datos_guardados.get("opiniones", [])
    except Exception as e:
        st.error(f"❌ Error al leer el archivo de opiniones: {e}")
        opiniones_existentes = []

    if not opiniones_existentes:
        st.info("ℹ️ No hay opiniones registradas aún en el archivo persistente.")
    else:
        # Fila de filtros
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            # Lista única de jugadores presentes en los registros
            nombres_en_db = sorted(list({op["jugador_nombre"] for op in opiniones_existentes if "jugador_nombre" in op}))
            filtro_jugador_nombre = st.selectbox(
                "🔍 Filtrar por Futbolista:",
                options=["Todos"] + nombres_en_db
            )
            
        with col_f2:
            filtro_sentimiento = st.selectbox(
                "🏷️ Filtrar por Sentimiento:",
                options=["Todos", "positivo", "negativo", "neutro", "mixto"]
            )
            
        # Determinar el jugador_id correspondiente si no es "Todos"
        jugador_id_filtro = None
        if filtro_jugador_nombre != "Todos":
            for op in opiniones_existentes:
                if op.get("jugador_nombre") == filtro_jugador_nombre:
                    jugador_id_filtro = op.get("jugador_id")
                    break

        # Ejecutar consulta y filtrado en memoria
        opiniones_filtradas = consultar_opiniones(
            registros=opiniones_existentes,
            jugador_id=jugador_id_filtro,
            sentimiento=None if filtro_sentimiento == "Todos" else filtro_sentimiento
        )
        
        # Conteo y desglose por categoría de los resultados filtrados
        total_filtradas = len(opiniones_filtradas)
        conteo_positivo = sum(1 for op in opiniones_filtradas if op.get("sentimiento") == "positivo")
        conteo_negativo = sum(1 for op in opiniones_filtradas if op.get("sentimiento") == "negativo")
        conteo_neutro = sum(1 for op in opiniones_filtradas if op.get("sentimiento") == "neutro")
        conteo_mixto = sum(1 for op in opiniones_filtradas if op.get("sentimiento") == "mixto")

        # Visualización de métricas
        st.markdown("### Resumen Estadístico")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("📋 Total Filtradas", total_filtradas)
        m2.metric("🟢 Positivos", conteo_positivo)
        m3.metric("🔴 Negativos", conteo_negativo)
        m4.metric("⚪ Neutros", conteo_neutro)
        m5.metric("🟡 Mixtos", conteo_mixto)

        st.markdown("---")

        if not opiniones_filtradas:
            st.warning("⚠️ No se encontraron opiniones que coincidan con los filtros seleccionados.")
        else:
            # Botón para descargar exactamente los datos filtrados en formato JSON
            json_exportable = json.dumps(opiniones_filtradas, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Descargar resultados filtrados (JSON)",
                data=json_exportable,
                file_name="tribuna_global_opiniones_filtradas.json",
                mime="application/json",
                use_container_width=True
            )

            st.markdown("### Detalle de Opiniones")
            # Presentar cada opinión con fecha, jugador, opinión original, sentimiento y razón
            for op in reversed(opiniones_filtradas):
                sent = op.get("sentimiento", "neutro")
                badge = BADGES_SENTIMIENTO.get(sent, sent)
                fecha_formato = op.get("fecha_utc", "")[:19].replace("T", " ")
                
                with st.expander(f"{badge} | {op.get('jugador_nombre')} | 📅 {fecha_formato} UTC", expanded=True):
                    st.markdown(f"**Opinión original:** *\"{op.get('opinion_original')}\"*")
                    st.markdown(f"**Justificación de IA:** {op.get('razon')}")
                    st.caption(
                        f"🆔 `{op.get('id')}` | 👤 ID Futbolista: `{op.get('jugador_id')}` | "
                        f"🤖 Modelo: `{op.get('modelo')}` | 📝 Versión Prompt: `{op.get('version_prompt')}`"
                    )
