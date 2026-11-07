"""
Script de pruebas unitarias para validar los requerimientos del Sprint 1
(Catálogo, Validación, Persistencia Atómica, Manejo de Archivos Dañados).
"""

import json
import os
import shutil
from pathlib import Path
import unittest

from almacenamiento import (
    cargar_jugadores,
    cargar_opiniones,
    crear_registro,
    guardar_opinion,
    consultar_opiniones,
    guardar_diccionario_atomico
)


class TestSprint1(unittest.TestCase):
    def setUp(self):
        # Crear un directorio temporal de pruebas para no alterar los datos reales
        self.test_dir = Path("test_sandbox_datos")
        self.test_dir.mkdir(exist_ok=True)
        self.test_opiniones = self.test_dir / "opiniones_test.json"
        self.test_jugadores = self.test_dir / "jugadores_test.json"

    def tearDown(self):
        # Limpiar directorio de pruebas
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_01_cargar_catalogo_oficial(self):
        """Verifica que el catálogo oficial tenga 20 jugadores y todos con IDs únicos."""
        jugadores = cargar_jugadores()
        self.assertGreaterEqual(len(jugadores), 20)
        
        ids = [j["id"] for j in jugadores]
        self.assertEqual(len(ids), len(set(ids)), "Existen identificadores de jugadores duplicados.")
        print("[OK] Test 1 superado: Catalogo oficial cargado con 20 jugadores y sin IDs repetidos.")

    def test_02_rechazo_catalogo_duplicado(self):
        """Verifica que si un catálogo tiene IDs repetidos, lance ValueError."""
        catalogo_invalido = {
            "version": 1,
            "jugadores": [
                {"id": "j001", "nombre": "Jugador Uno", "pais": "Pais A"},
                {"id": "j001", "nombre": "Jugador Dos", "pais": "Pais B"}
            ]
        }
        with open(self.test_jugadores, "w", encoding="utf-8") as f:
            json.dump(catalogo_invalido, f)

        with self.assertRaises(ValueError):
            cargar_jugadores(self.test_jugadores)
        print("[OK] Test 2 superado: Deteccion y rechazo de IDs duplicados en catalogo.")

    def test_03_inicializacion_archivo_inexistente(self):
        """Si el archivo de opiniones no existe, debe inicializarse automáticamente."""
        self.assertFalse(self.test_opiniones.exists())
        data = cargar_opiniones(self.test_opiniones)
        self.assertTrue(self.test_opiniones.exists())
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["opiniones"], [])
        print("[OK] Test 3 superado: Inicializacion automatica de archivo opiniones inexistente.")

    def test_04_proteccion_archivo_corrupto(self):
        """Si el archivo de opiniones está corrupto, NO debe borrarse ni sobreescribirse."""
        contenido_danado = "{ esto_no_es_un_json_valido: true "
        with open(self.test_opiniones, "w", encoding="utf-8") as f:
            f.write(contenido_danado)

        with self.assertRaises(ValueError):
            cargar_opiniones(self.test_opiniones)

        # Verificar que el contenido original NO se perdió ni se reemplazó por lista vacía
        with open(self.test_opiniones, "r", encoding="utf-8") as f:
            contenido_actual = f.read()
        self.assertEqual(contenido_actual, contenido_danado)
        print("[OK] Test 4 superado: Archivo dañado protegido contra sobreescritura silenciosa.")

    def test_05_crear_registro_y_guardado_atomico(self):
        """Verifica la generación de metadatos (UUID, fecha UTC) y la escritura atómica."""
        jugador = {"id": "j001", "nombre": "Lionel Messi"}
        analisis_mock = {"sentimiento": "positivo", "razon": "Elogio claro a su tecnica."}
        
        reg1 = crear_registro(jugador, "Es el mejor de la historia", analisis_mock, "gpt-4o-mini")
        
        self.assertTrue(len(reg1["id"]) > 10, "Debe tener un UUID valido")
        self.assertIn("T", reg1["fecha_utc"], "La fecha debe estar en formato ISO UTC")
        self.assertEqual(reg1["jugador_id"], "j001")
        self.assertEqual(reg1["jugador_nombre"], "Lionel Messi")
        self.assertEqual(reg1["version_prompt"], "1.0")

        # Guardar en disco
        guardar_opinion(self.test_opiniones, reg1)
        
        # Guardar una segunda opinión de otro jugador
        jugador2 = {"id": "j013", "nombre": "Luis Diaz"}
        analisis_mock2 = {"sentimiento": "positivo", "razon": "Destaca su velocidad."}
        reg2 = crear_registro(jugador2, "Gran desborde por la banda", analisis_mock2, "gpt-4o-mini")
        guardar_opinion(self.test_opiniones, reg2)

        # Re-guardar reg1 (simulando un reintento de la app)
        guardar_opinion(self.test_opiniones, reg1)

        # Verificar que solo hay 2 opiniones (no se duplicó reg1)
        datos_guardados = cargar_opiniones(self.test_opiniones)
        self.assertEqual(len(datos_guardados["opiniones"]), 2)
        print("[OK] Test 5 superado: Creacion de registro, persistencia atomica y prevencion de duplicados.")

    def test_06_consulta_y_filtros(self):
        """Verifica que las consultas en memoria filtren exactamente según los parámetros."""
        opiniones_ejemplo = [
            {"id": "1", "jugador_id": "j001", "sentimiento": "positivo", "razon": "..."},
            {"id": "2", "jugador_id": "j001", "sentimiento": "negativo", "razon": "..."},
            {"id": "3", "jugador_id": "j002", "sentimiento": "positivo", "razon": "..."},
            {"id": "4", "jugador_id": "j002", "sentimiento": "mixto", "razon": "..."},
        ]

        # Filtrar solo Messi
        res_messi = consultar_opiniones(opiniones_ejemplo, jugador_id="j001")
        self.assertEqual(len(res_messi), 2)

        # Filtrar solo positivos
        res_pos = consultar_opiniones(opiniones_ejemplo, sentimiento="positivo")
        self.assertEqual(len(res_pos), 2)

        # Filtrar CR7 + mixto
        res_cr7_mixto = consultar_opiniones(opiniones_ejemplo, jugador_id="j002", sentimiento="mixto")
        self.assertEqual(len(res_cr7_mixto), 1)

        # Filtrar todos
        res_todos = consultar_opiniones(opiniones_ejemplo, jugador_id="todos", sentimiento="todos")
        self.assertEqual(len(res_todos), 4)
        print("[OK] Test 6 superado: Consulta y filtrado por jugador y sentimiento.")


if __name__ == "__main__":
    unittest.main()
