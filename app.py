"""
Tribuna Global - Aplicación de Percepción de Futbolistas
Frontend de Alta Fidelidad impulsado por el Sistema de Diseño Google Stitch
("Pitch Obsidian & Stadium Luminescence") + LangChain & Pydantic.
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
    page_title="Ágora Colombia - Barómetro de Percepción Ciudadana",
    page_icon="🇨🇴",
    layout="wide"
)

# ---------------------------------------------------------
# SISTEMA DE DISEÑO GOOGLE STITCH ("Pitch Obsidian")
# Inyección de Google Fonts, Paleta Cyber-Stadium y Glassmorphism
# ---------------------------------------------------------
STITCH_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">

<style>
    /* Tipografía y Superficie Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(ellipse at 50% 0%, rgba(20, 34, 56, 0.5) 0%, rgba(5, 20, 36, 0.98) 100%), #051424 !important;
        color: #d4e4fa;
    }

    /* Barra lateral estilo Cabina VIP / VIP Suite */
    [data-testid="stSidebar"] {
        background: rgba(13, 28, 45, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.6);
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* Títulos con fuente Outfit */
    h1, h2, h3, .stHeading {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* Pestañas estilo Stadium Segmented Switcher */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(1, 15, 31, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 4px;
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        color: #94a3b8;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1c2b3c !important;
        color: #00f59b !important;
        border: 1px solid rgba(0, 245, 155, 0.35) !important;
        box-shadow: 0 0 16px rgba(0, 245, 155, 0.25);
    }

    /* Tarjetas Glassmorphism para mensajes de chat */
    .stitch-chat-card {
        background: rgba(14, 23, 38, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .stitch-chat-card:hover {
        border-color: rgba(0, 245, 155, 0.25);
        box-shadow: 0 6px 24px rgba(0, 245, 155, 0.08);
    }

    /* Botones primarios con pulso neón */
    .stButton > button[kind="primary"], .stButton > button {
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }

    /* Inputs y textareas */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(1, 15, 31, 0.85) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        color: #d4e4fa !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus {
        border-color: #00d2ff !important;
        box-shadow: 0 0 12px rgba(0, 210, 255, 0.25) !important;
    }

    /* Métricas con brillo Stitch */
    [data-testid="stMetric"] {
        background: rgba(14, 23, 38, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        color: #d4e4fa !important;
    }

    /* Expanders estilizados */
    .streamlit-expanderHeader {
        background-color: rgba(18, 33, 49, 0.6) !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
</style>
"""
st.markdown(STITCH_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# COMPONENTES VISUALES HTML STITCH
# ---------------------------------------------------------
def render_stitch_badge(sentimiento: str) -> str:
    """Genera las píldoras de sentimiento con efectos neón de Stitch."""
    sent = (sentimiento or "").lower().strip()
    if sent == "positivo":
        return """
        <span style="background: rgba(0, 245, 155, 0.12); color: #00F59B; border: 1px solid rgba(0, 245, 155, 0.35); padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.78rem; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 0 14px rgba(0,245,155,0.25);">
            <span style="width: 7px; height: 7px; border-radius: 50%; background: #00F59B; box-shadow: 0 0 8px #00F59B; display: inline-block;"></span>
            POSITIVO
        </span>
        """
    elif sent == "negativo":
        return """
        <span style="background: rgba(255, 59, 87, 0.12); color: #FF3B57; border: 1px solid rgba(255, 59, 87, 0.35); padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.78rem; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 0 14px rgba(255,59,87,0.25);">
            <span style="width: 7px; height: 7px; border-radius: 50%; background: #FF3B57; box-shadow: 0 0 8px #FF3B57; display: inline-block;"></span>
            NEGATIVO
        </span>
        """
    elif sent == "mixto":
        return """
        <span style="background: rgba(255, 183, 3, 0.12); color: #FFB703; border: 1px solid rgba(255, 183, 3, 0.35); padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.78rem; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 0 14px rgba(255,183,3,0.25);">
            <span style="width: 7px; height: 7px; border-radius: 50%; background: #FFB703; box-shadow: 0 0 8px #FFB703; display: inline-block;"></span>
            MIXTO
        </span>
        """
    else:  # neutro
        return """
        <span style="background: rgba(148, 163, 184, 0.12); color: #94A3B8; border: 1px solid rgba(148, 163, 184, 0.3); padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.78rem; display: inline-flex; align-items: center; gap: 6px;">
            <span style="width: 7px; height: 7px; border-radius: 50%; background: #94A3B8; display: inline-block;"></span>
            NEUTRO
        </span>
        """


# Mapeo de banderas emoji por país
BANDERAS = {
    "Argentina": "🇦🇷", "Portugal": "🇵🇹", "Brasil": "🇧🇷", "Francia": "🇫🇷",
    "Noruega": "🇳🇴", "Egipto": "🇪🇬", "Polonia": "🇵🇱", "Croacia": "🇭🇷",
    "Bélgica": "🇧🇪", "Uruguay": "🇺🇾", "Colombia": "🇨🇴", "Corea del Sur": "🇰🇷",
    "Senegal": "🇸🇳"
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
# 2. BARRA LATERAL (Cabina de Mando Stitch)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
        <div style="width: 42px; height: 42px; border-radius: 10px; background: rgba(0,245,155,0.12); border: 1px solid rgba(0,245,155,0.3); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; box-shadow: 0 0 15px rgba(0,245,155,0.25);">
            🇨🇴
        </div>
        <div>
            <div style="font-family: 'Outfit'; font-size: 1.3rem; font-weight: 800; color: #00F59B; line-height: 1.1; letter-spacing: -0.02em;">Ágora Colombia</div>
            <div style="font-size: 0.68rem; font-family: 'Inter'; font-weight: 700; color: #94a3b8; letter-spacing: 0.08em; text-transform: uppercase;">Barómetro de Percepción Ciudadana</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<p style='font-family: Outfit; font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: #cdffdc;'>👤 PRESIDENTES & LÍDERES</p>", unsafe_allow_html=True)
    
    # Formateo enriquecido con rol
    opciones_jugador = {}
    for j in catalogo_jugadores:
        etiqueta = f"🇨🇴 {j['nombre']} ({j.get('rol', j['pais'])})"
        opciones_jugador[etiqueta] = j
    
    seleccion_etiqueta = st.selectbox(
        "Selecciona el presidente o figura a opinar:",
        options=list(opciones_jugador.keys()),
        help="La opinión enviada se vinculará de forma atómica a esta figura pública."
    )
    jugador_seleccionado = opciones_jugador[seleccion_etiqueta]
    
    # Tarjeta de perfil Stitch del político seleccionado
    st.markdown(f"""
    <div style="background: rgba(1, 15, 31, 0.7); border: 1px solid rgba(0, 210, 255, 0.2); border-radius: 10px; padding: 12px; margin-top: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 1.4rem;">🇨🇴</span>
            <span style="background: rgba(0, 245, 155, 0.15); color: #00F59B; border: 1px solid rgba(0, 245, 155, 0.3); font-size: 0.65rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">MONITOR ACTIVO</span>
        </div>
        <div style="font-family: 'Outfit'; font-weight: 700; font-size: 1.05rem; color: #d4e4fa; margin-top: 4px;">{jugador_seleccionado['nombre']}</div>
        <div style="font-size: 0.72rem; color: #94a3b8; font-family: 'Inter'; margin-top: 4px;">
            <span>ID: <code style="color: #00d2ff;">{jugador_seleccionado['id']}</code></span> • 
            <span>{jugador_seleccionado.get('rol', 'Colombia')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<p style='font-family: Outfit; font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: #cdffdc;'>⚙️ MOTOR DE INFERENCIA</p>", unsafe_allow_html=True)
    
    # Detección de API Key
    env_api_key = os.getenv("OPENAI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    if env_api_key and env_api_key != "clave_configurada_localmente":
        api_key_activa = env_api_key
        if api_key_activa.startswith("AQ.") or api_key_activa.startswith("AIza") or "gemini" in os.getenv("OPENAI_MODEL", "").lower():
            st.markdown("""
            <div style="background: rgba(0, 245, 155, 0.1); border: 1px solid rgba(0, 245, 155, 0.3); border-radius: 8px; padding: 8px 12px; font-size: 0.75rem; color: #00f59b; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>🟢</span> Google Gemini AI Activo
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(0, 210, 255, 0.1); border: 1px solid rgba(0, 210, 255, 0.3); border-radius: 8px; padding: 8px 12px; font-size: 0.75rem; color: #00d2ff; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>🟢</span> OpenAI API Activa
            </div>
            """, unsafe_allow_html=True)
    else:
        api_key_activa = st.text_input(
            "API Key:",
            type="password",
            help="Ingresa tu clave de Google Gemini o OpenAI"
        )
    
    es_gemini = (
        api_key_activa.startswith("AQ.")
        or api_key_activa.startswith("AIza")
        or "gemini" in os.getenv("OPENAI_MODEL", "").lower()
    )
    
    opciones_modelos = (
        ["gemini-2.5-flash", "gemini-2.5-pro", "gpt-4o-mini", "gpt-4o"]
        if es_gemini
        else [DEFAULT_MODEL, "gpt-4o", "gemini-2.5-flash", "gpt-3.5-turbo"]
    )
    
    modelo_seleccionado = st.selectbox(
        "Modelo:",
        options=opciones_modelos,
        index=0
    )
    st.caption("ℹ️ **Temperatura:** `0.0` (Determinismo analítico estricto).")
    
    st.markdown("---")
    if st.button("🗑️ Nueva conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.toast("Sesión de chat reiniciada. Los registros persistidos se mantienen intactos.")
        st.rerun()

# ---------------------------------------------------------
# 3. GESTIÓN DEL ESTADO DE SESIÓN (st.session_state)
# ---------------------------------------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# ---------------------------------------------------------
# 4. ENCABEZADO STADIUM FLOODLIGHT
# ---------------------------------------------------------
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; background: rgba(1, 15, 31, 0.6); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px 24px; margin-bottom: 20px;">
    <div style="display: flex; align-items: center; gap: 14px;">
        <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(0, 245, 155, 0.15); border: 1px solid rgba(0, 245, 155, 0.4); display: flex; align-items: center; justify-content: center; font-size: 1.6rem; box-shadow: 0 0 20px rgba(0,245,155,0.25);">
            🇨🇴
        </div>
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 800; color: #d4e4fa; margin: 0; line-height: 1.2;">Ágora Colombia</h1>
            <p style="font-size: 0.8rem; color: #94a3b8; margin: 0; font-family: 'Inter';">Barómetro de Percepción sobre Presidentes de Colombia y Abelardo de la Espriella</p>
        </div>
    </div>
    <div style="display: flex; gap: 12px; align-items: center;">
        <span style="background: rgba(0, 245, 155, 0.12); color: #00F59B; border: 1px solid rgba(0, 245, 155, 0.3); font-size: 0.72rem; font-family: 'Inter'; font-weight: 700; padding: 4px 12px; border-radius: 9999px;">
            ● SISTEMA EN VIVO
        </span>
        <span style="background: rgba(0, 210, 255, 0.12); color: #00D2FF; border: 1px solid rgba(0, 210, 255, 0.3); font-size: 0.72rem; font-family: 'Inter'; font-weight: 700; padding: 4px 12px; border-radius: 9999px;">
            ⚡ LATENCIA: 24ms
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. PESTAÑAS PRINCIPALES STITCH
# ---------------------------------------------------------
tab_opinar, tab_consultar = st.tabs(["💬 Emitir Opinión (Chat en Vivo)", "📊 Consultar Opiniones (Auditoría & Métricas)"])

# =========================================================
# SECCIÓN 1: EMITIR OPINIÓN
# =========================================================
with tab_opinar:
    # Banner del jugador activo
    st.markdown(f"""
    <div style="background: rgba(14, 23, 38, 0.7); border-left: 3px solid #00F59B; border-radius: 10px; padding: 14px 18px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span style="font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; font-family: 'Inter'; font-weight: 700; letter-spacing: 0.05em;">Foco de Inferencia Actual</span>
                <div style="font-family: 'Outfit'; font-size: 1.35rem; font-weight: 800; color: #cdffdc;">{bandera_sel} {jugador_seleccionado['nombre']} <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 400;">({jugador_seleccionado['pais']})</span></div>
            </div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-family: 'Inter'; text-align: right;">
                Rango permitido: <strong>5 a 1000 caracteres</strong><br>
                <span style="color: #00d2ff;">Clasificación: Positivo • Negativo • Neutro • Mixto</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Renderizar historial visual con diseño Stitch Glassmorphism
    for msg in st.session_state.mensajes:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="stitch-chat-card" style="border-left: 3px solid #00D2FF;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-family: 'Outfit'; font-weight: 700; font-size: 0.95rem; color: #a5e7ff;">👤 Opinión de Aficionado sobre <strong>{msg.get('jugador_nombre', '')}</strong></span>
                    <span style="font-size: 0.7rem; font-family: 'Inter'; color: #849588;">Enviado</span>
                </div>
                <div style="font-size: 1rem; color: #d4e4fa; line-height: 1.5; font-style: italic;">
                    “{msg['content']}”
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if msg.get("es_pertinente", True):
                badge_html = render_stitch_badge(msg.get("sentimiento", "neutro"))
                guardado_html = """
                <span style="font-family: 'Inter'; font-size: 0.72rem; color: #00f59b; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                    💾 Persistido atómicamente en <code>opiniones.json</code>
                </span>
                """ if msg.get("guardado", False) else ""
                
                st.markdown(f"""
                <div class="stitch-chat-card" style="border-left: 3px solid #00F59B;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-family: 'Outfit'; font-weight: 700; font-size: 0.95rem; color: #00F59B; display: flex; align-items: center; gap: 6px;">
                            🤖 Clasificación de Inferencia AI
                        </span>
                        {badge_html}
                    </div>
                    <div style="background: rgba(1, 15, 31, 0.6); border-radius: 8px; padding: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 8px;">
                        <span style="font-size: 0.72rem; font-family: 'Inter'; text-transform: uppercase; color: #94a3b8; font-weight: 700;">Justificación Técnica:</span>
                        <p style="font-size: 0.92rem; color: #d4e4fa; margin: 4px 0 0 0; line-height: 1.4;">
                            {msg.get('razon', '')}
                        </p>
                    </div>
                    <div style="display: flex; justify-content: flex-end;">
                        {guardado_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="stitch-chat-card" style="border-left: 3px solid #FF3B57;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-family: 'Outfit'; font-weight: 700; font-size: 0.95rem; color: #FF3B57;">⚠️ Comentario No Pertinente Rechazado</span>
                        <span style="background: rgba(255, 59, 87, 0.12); color: #FF3B57; border: 1px solid rgba(255, 59, 87, 0.3); padding: 2px 10px; border-radius: 9999px; font-size: 0.7rem; font-weight: 700;">NO GUARDADO</span>
                    </div>
                    <p style="font-size: 0.92rem; color: #ffb4ab; margin: 0;">{msg.get('razon', '')}</p>
                    <p style="font-size: 0.75rem; color: #94a3b8; margin-top: 6px; font-family: 'Inter';">ℹ️ El texto no guarda relación con el futbolista. No se ha generado registro en disco.</p>
                </div>
                """, unsafe_allow_html=True)

    # Entrada de texto con st.chat_input
    texto_usuario = st.chat_input(f"Escribe tu opinión sobre el rendimiento o características de {jugador_seleccionado['nombre']}...")

    if texto_usuario:
        # Congelamiento estricto de la selección del jugador al momento del envío
        jugador_envio = {
            "id": jugador_seleccionado["id"],
            "nombre": jugador_seleccionado["nombre"],
            "pais": jugador_seleccionado["pais"]
        }
        
        # Validación de longitud (5 a 1000)
        try:
            texto_limpio = validar_texto_opinion(texto_usuario)
        except ValueError as ve:
            st.warning(f"⚠️ {ve}")
            st.stop()
            
        # Registrar y mostrar mensaje de usuario en pantalla
        st.session_state.mensajes.append({
            "role": "user",
            "content": texto_limpio,
            "jugador_id": jugador_envio["id"],
            "jugador_nombre": jugador_envio["nombre"]
        })
        
        with st.spinner("Ejecutando inferencia de sentimiento con IA..."):
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
                st.error(f"❌ Error de comunicación con el servicio de IA: {e}")
                st.info("💡 Tu opinión se mantiene en pantalla para que no pierdas lo que escribiste.")
                st.stop()

        # Evaluación de pertinencia y guardado condicional
        if not analisis.es_pertinente:
            st.session_state.mensajes.append({
                "role": "assistant",
                "content": analisis.razon,
                "es_pertinente": False,
                "sentimiento": None,
                "razon": analisis.razon,
                "guardado": False
            })
        else:
            try:
                registro = crear_registro(
                    jugador=jugador_envio,
                    texto=texto_limpio,
                    analisis=analisis,
                    modelo=modelo_seleccionado
                )
                guardar_opinion(RUTA_OPINIONES, registro)
                st.session_state.mensajes.append({
                    "role": "assistant",
                    "content": analisis.razon,
                    "es_pertinente": True,
                    "sentimiento": analisis.sentimiento,
                    "razon": analisis.razon,
                    "guardado": True
                })
            except Exception as err_escritura:
                st.error(f"❌ Error durante el almacenamiento atómico: {err_escritura}")

        st.rerun()


# =========================================================
# SECCIÓN 2: CONSULTAR OPINIONES (AUDITORÍA & TELEMETRÍA)
# =========================================================
with tab_consultar:
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h2 style="font-size: 1.4rem; font-weight: 800; color: #d4e4fa; margin: 0;">Base de Datos de Telemetría y Auditoría</h2>
        <p style="font-size: 0.85rem; color: #94a3b8; margin: 2px 0 0 0; font-family: 'Inter';">
            Registros persistidos en disco <code>opiniones.json</code> • <strong>Cero consumo de API en consultas</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        datos_guardados = cargar_opiniones(RUTA_OPINIONES)
        opiniones_existentes = datos_guardados.get("opiniones", [])
    except Exception as e:
        st.error(f"❌ Error al leer el archivo de opiniones: {e}")
        opiniones_existentes = []

    if not opiniones_existentes:
        st.info("ℹ️ No hay opiniones registradas aún en la base de datos.")
    else:
        # Fila de filtros Stitch
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
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
            
        jugador_id_filtro = None
        if filtro_jugador_nombre != "Todos":
            for op in opiniones_existentes:
                if op.get("jugador_nombre") == filtro_jugador_nombre:
                    jugador_id_filtro = op.get("jugador_id")
                    break

        # Consulta en memoria
        opiniones_filtradas = consultar_opiniones(
            registros=opiniones_existentes,
            jugador_id=jugador_id_filtro,
            sentimiento=None if filtro_sentimiento == "Todos" else filtro_sentimiento
        )
        
        # Conteos estadísticos
        total_filtradas = len(opiniones_filtradas)
        conteo_pos = sum(1 for op in opiniones_filtradas if op.get("sentimiento") == "positivo")
        conteo_neg = sum(1 for op in opiniones_filtradas if op.get("sentimiento") == "negativo")
        conteo_neu = sum(1 for op in opiniones_filtradas if op.get("sentimiento") == "neutro")
        conteo_mix = sum(1 for op in opiniones_filtradas if op.get("sentimiento") == "mixto")

        # 4 Tarjetas de Telemetría Neón estilo Stitch
        st.markdown("<p style='font-family: Outfit; font-weight: 700; font-size: 1rem; color: #a5e7ff; margin-top: 14px;'>PANEL DE TELEMETRÍA (FILTRADO)</p>", unsafe_allow_html=True)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("📋 Total Opiniones", total_filtradas)
        m2.metric("🟢 Positivos", conteo_pos)
        m3.metric("🔴 Negativos", conteo_neg)
        m4.metric("⚪ Neutros", conteo_neu)
        m5.metric("🟡 Mixtos", conteo_mix)

        st.markdown("---")

        if not opiniones_filtradas:
            st.warning("⚠️ No se encontraron opiniones que coincidan con los filtros seleccionados.")
        else:
            # Botón de Descarga JSON con estilo destacado
            col_cta1, col_cta2 = st.columns([2, 1])
            with col_cta1:
                st.markdown(f"<p style='font-size: 0.85rem; color: #94a3b8; font-family: Inter;'>Se exportarán <strong>{total_filtradas}</strong> registros correspondientes a la vista actual.</p>", unsafe_allow_html=True)
            with col_cta2:
                json_exportable = json.dumps(opiniones_filtradas, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 Descargar Telemetría (JSON)",
                    data=json_exportable,
                    file_name="tribuna_global_opiniones_filtradas.json",
                    mime="application/json",
                    use_container_width=True
                )

            st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700; color: #cdffdc; margin: 18px 0 10px 0;'>REGISTROS DE AUDITORÍA</h3>", unsafe_allow_html=True)
            
            # Despliegue de tarjetas de auditoría Stitch
            for op in reversed(opiniones_filtradas):
                sent = op.get("sentimiento", "neutro")
                badge_html = render_stitch_badge(sent)
                fecha_formato = op.get("fecha_utc", "")[:19].replace("T", " ")
                
                st.markdown(f"""
                <div class="stitch-chat-card" style="margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div>
                            <span style="font-family: 'Outfit'; font-weight: 700; font-size: 1.05rem; color: #d4e4fa;">
                                {op.get('jugador_nombre')}
                            </span>
                            <span style="font-size: 0.75rem; color: #94a3b8; font-family: 'Inter'; margin-left: 8px;">
                                📅 {fecha_formato} UTC
                            </span>
                        </div>
                        {badge_html}
                    </div>
                    <div style="font-size: 0.95rem; color: #d4e4fa; font-style: italic; margin-bottom: 8px; border-left: 2px solid rgba(0,210,255,0.4); padding-left: 10px;">
                        “{op.get('opinion_original')}”
                    </div>
                    <div style="background: rgba(1, 15, 31, 0.5); border-radius: 6px; padding: 8px 12px; font-size: 0.85rem; color: #b9cbbd; margin-bottom: 8px;">
                        <strong style="color: #cdffdc;">Justificación AI:</strong> {op.get('razon')}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.7rem; color: #849588; font-family: 'Inter';">
                        <span>🆔 <code>{op.get('id')}</code></span>
                        <span>🤖 {op.get('modelo')} • Prompt v{op.get('version_prompt')}</span>
                        <span style="color: #00f59b; font-weight: 600;">● Persistido</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
