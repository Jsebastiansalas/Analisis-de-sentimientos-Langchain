"""
Paquete de pruebas unitarias y de integración para Ágora Colombia / Tribuna Global.
Configura automáticamente sys.path para resolver las importaciones del proyecto raíz.
"""

import sys
from pathlib import Path

# Agregar la raíz del proyecto al sys.path para importar almacenamiento, analisis, etc.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))
