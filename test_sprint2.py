"""
Script de pruebas unitarias para validar los requerimientos del Sprint 2
(Pydantic Schema, Reglas de Negocio, Limpieza de Texto, Prompt con Roles y Blindaje).
"""

import unittest
from pydantic import ValidationError
from langchain_core.prompts import ChatPromptTemplate

from analisis import (
    AnalisisOpinion,
    validar_texto_opinion,
    validar_coherencia_analisis,
    crear_prompt_analisis,
    analizar_opinion,
    MIN_CARACTERES,
    MAX_CARACTERES
)


class TestSprint2(unittest.TestCase):

    def test_01_esquema_pydantic_valido(self):
        """Prueba que el modelo Pydantic acepte datos válidos para las 4 categorías y pertinencia."""
        # Caso positivo
        op_pos = AnalisisOpinion(es_pertinente=True, sentimiento="positivo", razon="Gran visión de juego.")
        self.assertTrue(op_pos.es_pertinente)
        self.assertEqual(op_pos.sentimiento, "positivo")

        # Caso negativo
        op_neg = AnalisisOpinion(es_pertinente=True, sentimiento="negativo", razon="Pobre rendimiento físico.")
        self.assertEqual(op_neg.sentimiento, "negativo")

        # Caso neutro
        op_neu = AnalisisOpinion(es_pertinente=True, sentimiento="neutro", razon="Mención fáctica de su rol.")
        self.assertEqual(op_neu.sentimiento, "neutro")

        # Caso mixto
        op_mix = AnalisisOpinion(es_pertinente=True, sentimiento="mixto", razon="Buen atacante pero mala actitud.")
        self.assertEqual(op_mix.sentimiento, "mixto")

        # Caso no pertinente (sentimiento null/None)
        op_no_per = AnalisisOpinion(es_pertinente=False, sentimiento=None, razon="Habla del clima, no del jugador.")
        self.assertFalse(op_no_per.es_pertinente)
        self.assertIsNone(op_no_per.sentimiento)
        print("[OK] Test 1 superado: Contrato Pydantic y categorias validas.")

    def test_02_restricciones_pydantic(self):
        """Verifica que Pydantic rechace sentimientos inventados o razones fuera de límite."""
        # Sentimiento no permitido
        with self.assertRaises(ValidationError):
            AnalisisOpinion(es_pertinente=True, sentimiento="excelente", razon="Muy bueno")

        # Razón vacía (mínimo 1 carácter)
        with self.assertRaises(ValidationError):
            AnalisisOpinion(es_pertinente=True, sentimiento="positivo", razon="")

        # Razón excesiva (> 300 caracteres)
        with self.assertRaises(ValidationError):
            AnalisisOpinion(es_pertinente=True, sentimiento="positivo", razon="A" * 301)

        print("[OK] Test 2 superado: Restricciones de longitud y tipos en Pydantic.")

    def test_03_reglas_de_negocio_pertinencia(self):
        """Valida la coherencia de negocio: no pertinente nunca tiene sentimiento y viceversa."""
        # Si no es pertinente pero el modelo por error devolvió sentimiento, se normaliza a None
        op_erronea = AnalisisOpinion(es_pertinente=False, sentimiento="positivo", razon="Habla de pizza.")
        op_corregida = validar_coherencia_analisis(op_erronea)
        self.assertIsNone(op_corregida.sentimiento, "Si es_pertinente=False, sentimiento debe ser None.")

        # Si es pertinente pero sentimiento es None, debe lanzar ValueError
        op_incompleta = AnalisisOpinion(es_pertinente=True, sentimiento=None, razon="Opinión válida.")
        with self.assertRaises(ValueError):
            validar_coherencia_analisis(op_incompleta)

        print("[OK] Test 3 superado: Reglas de coherencia de negocio entre pertinencia y sentimiento.")

    def test_04_limpieza_y_validacion_longitud_texto(self):
        """Verifica que el texto se limpie con strip() y cumpla entre 5 y 1000 caracteres."""
        # Texto muy corto (< 5 caracteres)
        with self.assertRaises(ValueError):
            validar_texto_opinion("Hola")

        # Texto solo espacios en blanco (se reduce a 0 caracteres)
        with self.assertRaises(ValueError):
            validar_texto_opinion("      ")

        # Texto que excede 1000 caracteres
        with self.assertRaises(ValueError):
            validar_texto_opinion("A" * 1001)

        # Texto válido con espacios en los extremos
        limpio = validar_texto_opinion("   Excelente precisión en los pases.   ")
        self.assertEqual(limpio, "Excelente precisión en los pases.")
        self.assertEqual(len(limpio), 33)

        print("[OK] Test 4 superado: Validacion de longitud (5 a 1000) y limpieza de texto.")

    def test_05_prompt_con_roles_y_blindaje(self):
        """Verifica que el prompt esté estructurado con roles (system/human) y contenga directrices clave."""
        prompt = crear_prompt_analisis()
        self.assertIsInstance(prompt, ChatPromptTemplate)

        mensajes = prompt.messages
        self.assertEqual(len(mensajes), 2, "El prompt debe tener exactamente 2 mensajes.")

        system_msg = mensajes[0].prompt.template
        human_msg = mensajes[1].prompt.template

        # Verificar rol system y directrices
        self.assertIn("ESTRICTAMENTE COMO DATOS", system_msg)
        self.assertIn("positivo", system_msg)
        self.assertIn("negativo", system_msg)
        self.assertIn("neutro", system_msg)
        self.assertIn("mixto", system_msg)
        self.assertIn("ironía", system_msg)
        self.assertIn("tercera persona", system_msg)

        # Verificar rol human (solo jugador y opinión, sin historial)
        self.assertIn("{jugador}", human_msg)
        self.assertIn("{opinion}", human_msg)
        self.assertNotIn("historial", human_msg, "El clasificador NO debe recibir historial previo.")

        print("[OK] Test 5 superado: Prompt con roles, criterios de clasificacion y defensa anti-inyeccion.")

    def test_06_error_sin_api_key_no_inventa_neutro(self):
        """Verifica que la ausencia de API key levante ValueError y no invente un sentimiento neutro."""
        with self.assertRaises(ValueError):
            analizar_opinion(
                jugador_nombre="Lionel Messi",
                texto_opinion="Excelente jugador de futbol",
                api_key=""
            )
        print("[OK] Test 6 superado: Fallo de API key lanza excepcion clara sin inventar registros.")


if __name__ == "__main__":
    unittest.main()
