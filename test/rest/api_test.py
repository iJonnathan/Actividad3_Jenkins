import unittest
import json
from unittest.mock import patch
import pytest

# Importamos la aplicación Flask directamente
from api import api_application


def mocked_validation(*args, **kwargs):
    """
    Función mock para simular la validación de permisos en las pruebas de API.
    Por defecto, devuelve True para permitir la operación.
    """
    return True

class TestAPI(unittest.TestCase):
    """
    Clase de pruebas de integración para la API de la calculadora.
    Utiliza el cliente de prueba de Flask para simular peticiones HTTP.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba de API.
        Crea un cliente de prueba para la aplicación Flask.
        """
        self.app = api_application.test_client()
        self.app.testing = True # Habilita el modo de prueba

    # --- Pruebas para la ruta principal ---
    def test_hello_route(self):
        """Verifica que la ruta principal devuelve el mensaje de bienvenida."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Hello from The Calculator!\n")
        # Aseguramos que el Content-Type sea text/plain como se espera en la prueba
        self.assertEqual(response.headers['Content-Type'], 'text/plain')


    # --- Pruebas para /calc/add ---
    def test_add_success(self):
        """Verifica que la ruta /calc/add funciona correctamente con números válidos."""
        response = self.app.get('/calc/add/5/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "8")

        response = self.app.get('/calc/add/2.5/3.5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "6.0")

    def test_add_failure_invalid_input(self):
        """Verifica que /calc/add devuelve 400 Bad Request con entrada inválida."""
        response = self.app.get('/calc/add/abc/3')
        self.assertEqual(response.status_code, 400)
        # El mensaje de error proviene de util.convert_to_number
        self.assertIn("Operator cannot be converted to number", response.data.decode())

    # --- Pruebas para /calc/substract ---
    def test_substract_success(self):
        """Verifica que la ruta /calc/substract funciona correctamente."""
        response = self.app.get('/calc/substract/10/4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "6")

        response = self.app.get('/calc/substract/5.5/2.5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "3.0")

    def test_substract_failure_invalid_input(self):
        """Verifica que /calc/substract devuelve 400 Bad Request con entrada inválida."""
        response = self.app.get('/calc/substract/10/xyz')
        self.assertEqual(response.status_code, 400)
        # El mensaje de error proviene de util.convert_to_number
        self.assertIn("Operator cannot be converted to number", response.data.decode())

    # --- Pruebas para /calc/multiply ---
    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_success(self, _mock_validate_permissions):
        """Verifica que la ruta /calc/multiply funciona correctamente."""
        response = self.app.get('/calc/multiply/6/7')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "42")

        response = self.app.get('/calc/multiply/2.5/4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "10.0")

    def test_multiply_failure_invalid_input(self):
        """Verifica que /calc/multiply devuelve 400 Bad Request con entrada inválida."""
        response = self.app.get('/calc/multiply/a/b')
        self.assertEqual(response.status_code, 400)
        # El mensaje de error proviene de util.convert_to_number
        self.assertIn("Operator cannot be converted to number", response.data.decode())

    @patch('app.util.validate_permissions', return_value=False, create=True)
    def test_multiply_failure_permissions(self, _mock_validate_permissions):
        """Verifica que /calc/multiply devuelve 400 Bad Request si no hay permisos."""
        response = self.app.get('/calc/multiply/2/2')
        # Ahora api.py captura InvalidPermissions y devuelve 400
        self.assertEqual(response.status_code, 400)
        self.assertIn("User has no permissions", response.data.decode())

    # --- Pruebas para /calc/divide ---
    def test_divide_success(self):
        """Verifica que la ruta /calc/divide funciona correctamente."""
        response = self.app.get('/calc/divide/10/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "5.0")

        response = self.app.get('/calc/divide/7/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "3.5")

    def test_divide_failure_division_by_zero(self):
        """Verifica que /calc/divide devuelve 400 Bad Request con división por cero."""
        response = self.app.get('/calc/divide/1/0')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Division by zero is not possible", response.data.decode())

    def test_divide_failure_invalid_input(self):
        """Verifica que /calc/divide devuelve 400 Bad Request con entrada inválida."""
        response = self.app.get('/calc/divide/10/zero')
        self.assertEqual(response.status_code, 400)
        # El mensaje de error proviene de util.convert_to_number
        self.assertIn("Operator cannot be converted to number", response.data.decode())

    # --- Pruebas para /calc/power ---
    def test_power_success(self):
        """Verifica que la ruta /calc/power funciona correctamente."""
        response = self.app.get('/calc/power/2/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "8")

        response = self.app.get('/calc/power/5/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "1")

        response = self.app.get('/calc/power/4/0.5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "2.0")

    def test_power_failure_invalid_input(self):
        """Verifica que /calc/power devuelve 400 Bad Request con entrada inválida."""
        response = self.app.get('/calc/power/x/2')
        self.assertEqual(response.status_code, 400)
        # El mensaje de error proviene de util.convert_to_number
        self.assertIn("Operator cannot be converted to number", response.data.decode())

    # --- Pruebas para /calc/sqrt ---
    def test_sqrt_success(self):
        """Verifica que la ruta /calc/sqrt funciona correctamente."""
        response = self.app.get('/calc/sqrt/9')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "3.0")

        response = self.app.get('/calc/sqrt/2.25')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "1.5")

    def test_sqrt_failure_negative_number(self):
        """Verifica que /calc/sqrt devuelve 400 Bad Request con número negativo."""
        response = self.app.get('/calc/sqrt/-4')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Cannot calculate the square root of a negative number", response.data.decode())

    def test_sqrt_failure_invalid_input(self):
        """Verifica que /calc/sqrt devuelve 400 Bad Request con entrada inválida."""
        response = self.app.get('/calc/sqrt/invalid')
        self.assertEqual(response.status_code, 400)
        # El mensaje de error proviene de util.convert_to_number
        self.assertIn("Operator cannot be converted to number", response.data.decode())

    # --- Pruebas para /calc/log10 ---
    def test_log10_success(self):
        """Verifica que la ruta /calc/log10 funciona correctamente."""
        response = self.app.get('/calc/log10/100')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "2.0")

        response = self.app.get('/calc/log10/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "0.0")

        response = self.app.get('/calc/log10/0.1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "-1.0")

    def test_log10_failure_non_positive_number(self):
        """Verifica que /calc/log10 devuelve 400 Bad Request con número no positivo."""
        response = self.app.get('/calc/log10/0')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Cannot calculate the base 10 logarithm of a non-positive number", response.data.decode())

        response = self.app.get('/calc/log10/-10')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Cannot calculate the base 10 logarithm of a non-positive number", response.data.decode())

    def test_log10_failure_invalid_input(self):
        """Verifica que /calc/log10 devuelve 400 Bad Request con entrada inválida."""
        response = self.app.get('/calc/log10/text')
        self.assertEqual(response.status_code, 400)
        # El mensaje de error proviene de util.convert_to_number
        self.assertIn("Operator cannot be converted to number", response.data.decode())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
