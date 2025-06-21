import unittest
from unittest.mock import patch
import pytest

from app.calc import Calculator


def mocked_validation(*args, **kwargs):
    return True


class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.add(2, 2))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))

    #def test_divide_method_returns_correct_result(self):
    #    self.assertEqual(1, self.calc.divide(2, 2))
    #    self.assertEqual(1.5, self.calc.divide(3, 2))

    def test_add_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.add, "2", 2)
        self.assertRaises(TypeError, self.calc.add, 2, "2")
        self.assertRaises(TypeError, self.calc.add, "2", "2")
        self.assertRaises(TypeError, self.calc.add, None, 2)
        self.assertRaises(TypeError, self.calc.add, 2, None)
        self.assertRaises(TypeError, self.calc.add, object(), 2)
        self.assertRaises(TypeError, self.calc.add, 2, object())

    #def test_divide_method_fails_with_nan_parameter(self):
    #    self.assertRaises(TypeError, self.calc.divide, "2", 2)
    #    self.assertRaises(TypeError, self.calc.divide, 2, "2")
    #    self.assertRaises(TypeError, self.calc.divide, "2", "2")

    def test_divide_method_fails_with_division_by_zero(self):
        self.assertRaises(TypeError, self.calc.divide, 2, 0)
        self.assertRaises(TypeError, self.calc.divide, 2, -0)
        self.assertRaises(TypeError, self.calc.divide, 0, 0)
        self.assertRaises(TypeError, self.calc.divide, "0", 0)

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(4, self.calc.multiply(2, 2))
        self.assertEqual(0, self.calc.multiply(1, 0))
        self.assertEqual(0, self.calc.multiply(-1, 0))
        self.assertEqual(-2, self.calc.multiply(-1, 2))

    #more mothods
    # --- Pruebas de la función substract ---
    def test_substract_method_returns_correct_result(self):
        """Verifica que el método substract devuelve el resultado correcto."""
        self.assertEqual(0, self.calc.substract(2, 2))
        self.assertEqual(4, self.calc.substract(2, -2))
        self.assertEqual(-4, self.calc.substract(-2, 2))
        self.assertEqual(1, self.calc.substract(1, 0))
        self.assertEqual(-0.5, self.calc.substract(2.5, 3))
        self.assertEqual(0.5, self.calc.substract(-2.5, -3))

    def test_substract_method_fails_with_nan_parameter(self):
        """Verifica que el método substract falla con parámetros no numéricos."""
        self.assertRaises(TypeError, self.calc.substract, "2", 2)
        self.assertRaises(TypeError, self.calc.substract, 2, "2")
        self.assertRaises(TypeError, self.calc.substract, None, 2)

    

    # --- Pruebas de la función divide ---
    def test_divide_method_returns_correct_result(self):
        """Verifica que el método divide devuelve el resultado correcto."""
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))
        self.assertEqual(-1, self.calc.divide(2, -2))
        self.assertEqual(0.5, self.calc.divide(1, 2))
        self.assertEqual(0, self.calc.divide(0, 5))
        self.assertAlmostEqual(0.8333333333333334, self.calc.divide(2.5, 3))

    def test_divide_method_fails_with_nan_parameter(self):
        """Verifica que el método divide falla con parámetros no numéricos."""
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")
        self.assertRaises(TypeError, self.calc.divide, None, 2)

    # MORE Y MORE TEST
    # --- Pruebas de la función power ---
    def test_power_method_returns_correct_result(self):
        """Verifica que el método power devuelve el resultado correcto."""
        self.assertEqual(4, self.calc.power(2, 2))
        self.assertEqual(8, self.calc.power(2, 3))
        self.assertEqual(1, self.calc.power(5, 0))
        self.assertEqual(0.25, self.calc.power(2, -2))
        self.assertEqual(9, self.calc.power(-3, 2))
        self.assertEqual(-27, self.calc.power(-3, 3))
        self.assertAlmostEqual(2.25, self.calc.power(1.5, 2))

    def test_power_method_fails_with_nan_parameter(self):
        """Verifica que el método power falla con parámetros no numéricos."""
        self.assertRaises(TypeError, self.calc.power, "2", 2)
        self.assertRaises(TypeError, self.calc.power, 2, "2")
        self.assertRaises(TypeError, self.calc.power, None, 2)

    # --- Pruebas de la función sqrt ---
    def test_sqrt_method_returns_correct_result(self):
        """Verifica que el método sqrt devuelve el resultado correcto."""
        self.assertEqual(2, self.calc.sqrt(4))
        self.assertEqual(0, self.calc.sqrt(0))
        self.assertAlmostEqual(1.41421356237, self.calc.sqrt(2), places=10)
        self.assertAlmostEqual(2.2360679775, self.calc.sqrt(5), places=10)
        self.assertAlmostEqual(1.5, self.calc.sqrt(2.25))

    def test_sqrt_method_fails_with_nan_parameter(self):
        """Verifica que el método sqrt falla con parámetros no numéricos."""
        self.assertRaises(TypeError, self.calc.sqrt, "4")
        self.assertRaises(TypeError, self.calc.sqrt, None)
        self.assertRaises(TypeError, self.calc.sqrt, object())

    def test_sqrt_method_fails_with_negative_number(self):
        """Verifica que el método sqrt falla con números negativos."""
        self.assertRaises(ValueError, self.calc.sqrt, -1)
        self.assertRaises(ValueError, self.calc.sqrt, -4)
        self.assertRaises(ValueError, self.calc.sqrt, -0.001)

    # --- Pruebas de la función log10 ---
    def test_log10_method_returns_correct_result(self):
        """Verifica que el método log10 devuelve el resultado correcto."""
        self.assertEqual(1, self.calc.log10(10))
        self.assertEqual(2, self.calc.log10(100))
        self.assertAlmostEqual(0, self.calc.log10(1), places=10)
        self.assertAlmostEqual(0.30102999566, self.calc.log10(2), places=10)
        self.assertAlmostEqual(-1, self.calc.log10(0.1), places=10)
        self.assertAlmostEqual(0.39794000867, self.calc.log10(2.5), places=10)

    def test_log10_method_fails_with_nan_parameter(self):
        """Verifica que el método log10 falla con parámetros no numéricos."""
        self.assertRaises(TypeError, self.calc.log10, "10")
        self.assertRaises(TypeError, self.calc.log10, None)
        self.assertRaises(TypeError, self.calc.log10, object())

    def test_log10_method_fails_with_non_positive_number(self):
        """Verifica que el método log10 falla con números no positivos."""
        self.assertRaises(ValueError, self.calc.log10, 0)
        self.assertRaises(ValueError, self.calc.log10, -1)
        self.assertRaises(ValueError, self.calc.log10, -100)
        self.assertRaises(ValueError, self.calc.log10, -0.001)

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
