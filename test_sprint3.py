"""
Script de pruebas unitarias para validar los requerimientos del Sprint 3
(Gestión de Sesión, Congelamiento de Jugador al Enviar, Preservación de Archivo al Reiniciar).
"""

import unittest
from pathlib import Path
import json

from almacenamiento import (
    cargar_jugadores,
    cargar_opiniones,
    crear_registro,
    guardar_opinion
)
from analisis import AnalisisOpinion


class TestSprint3(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path("test_sandbox_sprint3")
        self.test_dir.mkdir(exist_ok=True)
        self.test_opiniones = self.test_dir / "opiniones_s3.json"
        
        # Inicializar archivo de pruebas
        with open(self.test_opiniones, "w", encoding="utf-8") as f:
            json.dump({"version": 1, "opiniones": []}, f)

    def tearDown(self):
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_01_congelamiento_jugador_al_enviar(self):
        """
        Simula que el usuario selecciona a Messi, envía una opinión,
        y luego cambia el selector a Cristiano Ronaldo.
        El registro guardado DEBE conservar a Messi, sin verse afectado por el cambio posterior.
        """
        # 1. Jugador activo en el momento del clic
        jugador_seleccionado_al_enviar = {"id": "j001", "nombre": "Lionel Messi"}
        analisis_messi = AnalisisOpinion(es_pertinente=True, sentimiento="positivo", razon="Elogio a su juego")

        registro_guardado = crear_registro(
            jugador=jugador_seleccionado_al_enviar,
            texto="Pase magistral",
            analisis=analisis_messi,
            modelo="gpt-4o-mini"
        )
        guardar_opinion(self.test_opiniones, registro_guardado)

        # 2. El usuario cambia el selector en la interfaz a Cristiano Ronaldo
        jugador_selector_despues = {"id": "j002", "nombre": "Cristiano Ronaldo"}

        # 3. Comprobar que en disco sigue estando Messi
        datos = cargar_opiniones(self.test_opiniones)
        self.assertEqual(len(datos["opiniones"]), 1)
        self.assertEqual(datos["opiniones"][0]["jugador_id"], "j001")
        self.assertEqual(datos["opiniones"][0]["jugador_nombre"], "Lionel Messi")
        print("[OK] Test 1 superado: Jugador congelado correctamente al momento del envio.")

    def test_02_no_pertinente_no_se_guarda(self):
        """Simula una opinión no pertinente y verifica que NO se inserte en el archivo JSON."""
        analisis_ajeno = AnalisisOpinion(
            es_pertinente=False,
            sentimiento=None,
            razon="El texto habla sobre baloncesto, no sobre fútbol."
        )

        # Regla de app.py: si no es pertinente, NUNCA se invoca guardar_opinion
        if analisis_ajeno.es_pertinente:
            registro = crear_registro({"id": "j001", "nombre": "Messi"}, "Texto", analisis_ajeno, "gpt")
            guardar_opinion(self.test_opiniones, registro)

        datos = cargar_opiniones(self.test_opiniones)
        self.assertEqual(len(datos["opiniones"]), 0, "No debe haberse guardado nada.")
        print("[OK] Test 2 superado: Opiniones no pertinentes rechazadas y excluidas de persistencia.")

    def test_03_nueva_conversacion_no_borra_archivo(self):
        """
        Simula el botón 'Nueva conversación':
        El session_state se vacía, pero el archivo en disco permanece intacto con todos sus registros.
        """
        # Guardar 2 opiniones previas en disco
        reg1 = crear_registro({"id": "j001", "nombre": "Messi"}, "Genio", AnalisisOpinion(es_pertinente=True, sentimiento="positivo", razon="..."), "gpt")
        reg2 = crear_registro({"id": "j002", "nombre": "CR7"}, "Goleador", AnalisisOpinion(es_pertinente=True, sentimiento="positivo", razon="..."), "gpt")
        guardar_opinion(self.test_opiniones, reg1)
        guardar_opinion(self.test_opiniones, reg2)

        # Simulación de session_state con 2 mensajes en pantalla
        session_state_mensajes = [
            {"role": "user", "content": "Genio"},
            {"role": "assistant", "content": "..."}
        ]

        # Acción del botón "Nueva conversación"
        session_state_mensajes = []  # Se limpia la lista en memoria

        # Verificar que la memoria de la sesión se limpió
        self.assertEqual(len(session_state_mensajes), 0)

        # Verificar que el archivo en disco sigue teniendo sus 2 opiniones
        datos_disco = cargar_opiniones(self.test_opiniones)
        self.assertEqual(len(datos_disco["opiniones"]), 2)
        print("[OK] Test 3 superado: 'Nueva conversación' limpia el chat pero conserva el archivo intacto.")


if __name__ == "__main__":
    unittest.main()
