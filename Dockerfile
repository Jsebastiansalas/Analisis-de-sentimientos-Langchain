# =========================================================
# DOCKERFILE - TRIBUNA GLOBAL
# Imagen ligera, segura y optimizada para producción
# =========================================================

# 1. Imagen base oficial de Python (versión estable y ligera)
FROM python:3.11-slim

# Metadatos del proyecto
LABEL maintainer="Tribuna Global Team"
LABEL description="Chatbot de Percepción de Futbolistas con Streamlit, LangChain y Salida Estructurada"

# 2. Variables de entorno de Python y Streamlit
# - PYTHONUNBUFFERED: Los prints y logs aparecen en la terminal en tiempo real sin demoras
# - PYTHONDONTWRITEBYTECODE: Evita generar archivos .pyc dentro del contenedor
# - STREAMLIT_*: Configura Streamlit para correr en contenedores sin requerir interacción manual
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 3. Instalar herramientas mínimas del sistema operativo (curl para healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Crear usuario no privilegiado por seguridad (Best Practice)
# Ejecutar contenedores como 'root' es un riesgo de seguridad en producción
RUN useradd -m -u 1000 appuser

# 5. Directorio de trabajo
WORKDIR /app

# 6. Instalar dependencias de Python aprovechando la caché de Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copiar el código de la aplicación
COPY . /app

# 8. Ajustar permisos para que el usuario no-root pueda escribir en /app/datos
RUN chown -R appuser:appuser /app

# 9. Cambiar al usuario seguro
USER appuser

# 10. Puerto de Streamlit
EXPOSE 8501

# 11. Healthcheck para verificar que la aplicación esté respondiendo
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 12. Comando de arranque
CMD ["streamlit", "run", "app.py"]
