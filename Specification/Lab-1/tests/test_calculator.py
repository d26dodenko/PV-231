from contextlib import redirect_stdout, redirect_stderr
from decimal import Decimal, localcontext
from io import StringIO
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

from calculator import calculate, main


class CalculatorTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate(Decimal("0.1"), "+", Decimal("0.2")), Decimal("0.3"))

    def test_subtraction(self):
        self.assertEqual(calculate(Decimal("2"), "-", Decimal("5")), Decimal("-3"))

    def test_multiplication(self):
        self.assertEqual(calculate(Decimal("-1.5"), "*", Decimal("4")), Decimal("-6"))

    def test_division(self):
        self.assertEqual(calculate(Decimal("7"), "/", Decimal("2")), Decimal("3.5"))

    def test_recurring_fraction(self):
        self.assertEqual(calculate(Decimal(1), "/", Decimal(3)), Decimal("0." + "3" * 28))

    def test_zero_divisor(self):
        for zero in ("0", "-0", "0.000"):
            with self.subTest(zero=zero), self.assertRaisesRegex(ZeroDivisionError, "ноль"):
                calculate(Decimal(1), "/", Decimal(zero))

    def test_zero_numerator(self):
        self.assertEqual(calculate(Decimal(0), "/", Decimal(2)), Decimal(0))

    def test_unknown_operation(self):
        with self.assertRaisesRegex(ValueError, "Неизвестная операция"):
            calculate(Decimal(1), "%", Decimal(2))

    def test_nonfinite_left(self):
        for value in ("NaN", "sNaN", "Infinity", "-Infinity"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                calculate(Decimal(value), "+", Decimal(1))

    def test_nonfinite_right(self):
        for value in ("NaN", "sNaN", "Infinity", "-Infinity"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                calculate(Decimal(1), "+", Decimal(value))

    def test_context_isolation(self):
        with localcontext() as context:
            context.prec = 3
            self.assertEqual(calculate(Decimal(1), "/", Decimal(3)), Decimal("0." + "3" * 28))
            self.assertEqual(context.prec, 3)


class InteractiveInputTests(unittest.TestCase):
    def invoke(self, values):
        output, errors = StringIO(), StringIO()
        with patch("builtins.input", side_effect=values), redirect_stdout(output), redirect_stderr(errors):
            code = main()
        return code, output.getvalue(), errors.getvalue()

    def test_success(self):
        self.assertEqual(self.invoke(["0.1", "+", "0.2"]), (0, "Результат: 0.3\n", ""))

    def test_negative_numbers(self):
        self.assertEqual(self.invoke(["-2", "*", "-3"]), (0, "Результат: 6\n", ""))

    def test_invalid_number(self):
        for value in ("abc", "", "1,5"):
            with self.subTest(value=value):
                code, output, errors = self.invoke([value, "+", "1"])
                self.assertEqual((code, output), (2, ""))
                self.assertIn("Ошибка:", errors)

    def test_division_error(self):
        code, output, errors = self.invoke(["1", "/", "0"])
        self.assertEqual((code, output), (2, ""))
        self.assertIn("Деление на ноль", errors)

    def test_nonfinite_error(self):
        code, output, errors = self.invoke(["NaN", "+", "1"])
        self.assertEqual((code, output), (2, ""))
        self.assertIn("конечными", errors)

    def test_overflow_error(self):
        code, output, errors = self.invoke(["1e999999", "*", "10"])
        self.assertEqual((code, output), (2, ""))
        self.assertIn("Ошибка:", errors)

    def test_invalid_second_number(self):
        code, output, errors = self.invoke(["1", "+", "abc"])
        self.assertEqual((code, output), (2, ""))
        self.assertIn("некорректное число", errors)

    def test_unknown_operation(self):
        code, output, errors = self.invoke(["1", "%", "2"])
        self.assertEqual((code, output), (2, ""))
        self.assertIn("Неизвестная операция", errors)

    def test_end_of_input(self):
        for values in ([EOFError], ["1", EOFError], ["1", "+", EOFError]):
            with self.subTest(values=values):
                self.assertEqual(self.invoke(values), (2, "", "Ошибка: ввод прерван\n"))

    def test_keyboard_interrupt(self):
        self.assertEqual(self.invoke([KeyboardInterrupt]), (2, "", "Ошибка: ввод прерван\n"))

    def test_surrounding_whitespace(self):
        self.assertEqual(self.invoke([" 2 ", " * ", " 3 "]), (0, "Результат: 6\n", ""))

    def test_script_entrypoint(self):
        script = Path(__file__).resolve().parents[1] / "calculator.py"
        with patch("sys.stdin", StringIO("2\n+\n3\n")):
            output = StringIO()
            with redirect_stdout(output), self.assertRaises(SystemExit) as raised:
                runpy.run_path(str(script), run_name="__main__")
        self.assertEqual(raised.exception.code, 0)
        self.assertEqual(output.getvalue(), "Введите первое число: Введите операцию (+, -, *, /): Введите второе число: Результат: 5\n")
