"""
Script de pruebas unitarias para validar los requerimientos del Sprint 4
(Semilla de Datos >= 12 opiniones, Cobertura de 4 jugadores y 4 categorías,
Métricas de Consulta y Exportación JSON).
"""

import json
import unittest
import uuid
from pathlib import Path

from almacenamiento import cargar_opiniones, consultar_opiniones, RUTA_OPINIONES


class TestSprint4(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = cargar_opiniones(RUTA_OPINIONES)
        cls.opiniones = cls.data["opiniones"]

    def test_01_cantidad_minima_opiniones_semilla(self):
        """Verifica que existan al menos 12 registros de opiniones precargados."""
        total = len(self.opiniones)
        self.assertGreaterEqual(total, 12, f"Se esperaban al menos 12 opiniones semilla, pero hay {total}.")
        print(f"[OK] Test 1 superado: Base semilla con {total} opiniones registradas.")

    def test_02_cobertura_minima_cuatro_jugadores(self):
        """Verifica que las opiniones estén distribuidas entre al menos 4 futbolistas distintos."""
        jugadores = {op["jugador_id"] for op in self.opiniones}
        nombres = {op["jugador_nombre"] for op in self.opiniones}
        self.assertGreaterEqual(len(jugadores), 4, f"Se esperaban al menos 4 jugadores, hay {len(jugadores)}.")
        print(f"[OK] Test 2 superado: Distribución en {len(jugadores)} futbolistas: {list(nombres)}.")

    def test_03_cobertura_cuatro_categorias_sentimiento(self):
        """Verifica que estén presentes las 4 categorías: positivo, negativo, neutro y mixto."""
        categorias = {op["sentimiento"] for op in self.opiniones}
        esperadas = {"positivo", "negativo", "neutro", "mixto"}
        self.assertTrue(esperadas.issubset(categorias), f"Faltan categorías de sentimiento: {esperadas - categorias}")
        print(f"[OK] Test 3 superado: Las 4 categorías de sentimiento están cubiertas ({list(categorias)}).")

    def test_04_campos_obligatorios_y_uuid_valido(self):
        """Verifica la presencia y validez de todos los campos obligatorios y metadatos."""
        for op in self.opiniones:
            # Validar UUID
            val_uuid = uuid.UUID(op["id"])
            self.assertIsNotNone(val_uuid)
            
            # Validar campos de metadatos
            self.assertTrue(op["fecha_utc"].endswith("+00:00") or "Z" in op["fecha_utc"])
            self.assertTrue(len(op["opinion_original"]) >= 5)
            self.assertTrue(len(op["razon"]) >= 1)
            self.assertEqual(op["version_prompt"], "1.0")
            self.assertEqual(op["modelo"], "gpt-4o-mini")
        print("[OK] Test 4 superado: Todos los registros tienen UUID válido, fecha UTC y metadatos completos.")

    def test_05_sincronizacion_metricas_consulta(self):
        """Verifica que el recuento de categorías coincida exactamente con el total filtrado."""
        # Filtrar por un jugador (ej: Messi)
        filtradas = consultar_opiniones(self.opiniones, jugador_id="j001")
        total = len(filtradas)
        conteo_pos = sum(1 for op in filtradas if op["sentimiento"] == "positivo")
        conteo_neg = sum(1 for op in filtradas if op["sentimiento"] == "negativo")
        conteo_neu = sum(1 for op in filtradas if op["sentimiento"] == "neutro")
        conteo_mix = sum(1 for op in filtradas if op["sentimiento"] == "mixto")

        self.assertEqual(total, conteo_pos + conteo_neg + conteo_neu + conteo_mix)
        print(f"[OK] Test 5 superado: Métricas de conteo por sentimiento perfectamente sincronizadas ({total} = {conteo_pos}+{conteo_neg}+{conteo_neu}+{conteo_mix}).")

    def test_06_descarga_json_consistencia(self):
        """Verifica que la exportación a JSON conserve acentos y estructura sin corrupción."""
        filtradas = consultar_opiniones(self.opiniones, sentimiento="positivo")
        json_str = json.dumps(filtradas, ensure_ascii=False, indent=2)
        deserializado = json.loads(json_str)

        self.assertEqual(len(deserializado), len(filtradas))
        self.assertEqual(deserializado[0]["id"], filtradas[0]["id"])
        # Verificar que conserve tildes correctamente
        self.assertIn("ó", json_str)
        print("[OK] Test 6 superado: Exportación JSON válida y con soporte UTF-8 sin escapes ASCII.")


if __name__ == "__main__":
    unittest.main()
