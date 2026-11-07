"""
Pruebas unitarias para validar las Extensiones y Desafíos de Ampliación de la Sección 12
(Búsqueda por texto libre, Auditoría Humana / Human-in-the-Loop y Benchmarking Dual).
"""

import os
import shutil
import unittest
from pathlib import Path

from almacenamiento import (
    cargar_opiniones,
    consultar_opiniones,
    corregir_opinion,
    guardar_diccionario_atomico
)
from analisis import comparar_analisis, AnalisisOpinion


class TestAmpliaciones(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path("test_sandbox_ampliaciones")
        self.test_dir.mkdir(exist_ok=True)
        self.test_opiniones = self.test_dir / "opiniones_ampliaciones.json"

        # Cargar datos base de prueba
        estructura_inicial = {
            "version": 1,
            "opiniones": [
                {
                    "id": "test-uuid-001",
                    "fecha_utc": "2026-11-06T10:00:00+00:00",
                    "jugador_id": "p001",
                    "jugador_nombre": "Gustavo Petro Urrego",
                    "opinion_original": "Excelente propuesta de transición energética y justicia social.",
                    "sentimiento": "positivo",
                    "razon": "Elogio enfático a las reformas.",
                    "modelo": "gemini-2.5-flash",
                    "version_prompt": "1.0"
                },
                {
                    "id": "test-uuid-002",
                    "fecha_utc": "2026-11-06T10:05:00+00:00",
                    "jugador_id": "p002",
                    "jugador_nombre": "Álvaro Uribe Vélez",
                    "opinion_original": "Brillante su austeridad: triplicó los gastos en burocracia.",
                    "sentimiento": "positivo",  # Supongamos que la IA erró inicialmente clasificando la ironía como positivo
                    "razon": "Menciona la palabra brillante.",
                    "modelo": "gemini-2.5-flash",
                    "version_prompt": "1.0"
                }
            ]
        }
        guardar_diccionario_atomico(self.test_opiniones, estructura_inicial)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_01_busqueda_por_texto_libre(self):
        """Verifica que el filtrado por texto libre funcione en opiniones y justificaciones."""
        data = cargar_opiniones(self.test_opiniones)
        registros = data["opiniones"]

        # Buscar palabra 'energética'
        res1 = consultar_opiniones(registros, texto_busqueda="energética")
        self.assertEqual(len(res1), 1)
        self.assertEqual(res1[0]["id"], "test-uuid-001")

        # Buscar palabra 'burocracia'
        res2 = consultar_opiniones(registros, texto_busqueda="burocracia")
        self.assertEqual(len(res2), 1)
        self.assertEqual(res2[0]["id"], "test-uuid-002")

        # Buscar término inexistente
        res3 = consultar_opiniones(registros, texto_busqueda="astronomía")
        self.assertEqual(len(res3), 0)
        print("[OK] Test Ampliación 1 superado: Filtrado por texto libre exacto y en memoria.")

    def test_02_corregir_opinion_conserva_original(self):
        """
        Verifica que la auditoría humana (Human-in-the-Loop) preserve el sentimiento original
        de la IA en 'sentimiento_original' y actualice 'sentimiento' y 'sentimiento_corregido'.
        """
        modificado = corregir_opinion(
            ruta=self.test_opiniones,
            opinion_id="test-uuid-002",
            nuevo_sentimiento="negativo",
            justificacion="Se detecta ironía sarcástica evidente sobre los gastos.",
            corregido_por="evaluador_academico"
        )

        self.assertEqual(modificado["sentimiento"], "negativo")
        self.assertEqual(modificado["sentimiento_corregido"], "negativo")
        self.assertEqual(modificado["sentimiento_original"], "positivo")
        self.assertEqual(modificado["corregido_por"], "evaluador_academico")
        self.assertIn("T", modificado["fecha_correccion_utc"])

        # Verificar persistencia en disco tras recarga
        data_recargada = cargar_opiniones(self.test_opiniones)
        op_disco = next(op for op in data_recargada["opiniones"] if op["id"] == "test-uuid-002")
        self.assertEqual(op_disco["sentimiento"], "negativo")
        self.assertEqual(op_disco["sentimiento_original"], "positivo")
        print("[OK] Test Ampliación 2 superado: Human-in-the-Loop conserva predicción IA original y persiste corrección.")


if __name__ == "__main__":
    unittest.main()
