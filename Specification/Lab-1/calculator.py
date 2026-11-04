from decimal import Decimal, DecimalException, localcontext
import sys


def calculate(a: Decimal, operation: str, b: Decimal) -> Decimal:
    if not a.is_finite() or not b.is_finite():
        raise ValueError("Операнды должны быть конечными числами")
    with localcontext() as context:
        context.prec = 28
        if operation == "+":
            return a + b
        if operation == "-":
            return a - b
        if operation == "*":
            return a * b
        if operation == "/":
            if b == 0:
                raise ZeroDivisionError("Деление на ноль запрещено")
            return a / b
    raise ValueError("Неизвестная операция: " + operation)


def main() -> int:
    try:
        a = Decimal(input("Введите первое число: ").strip())
        operation = input("Введите операцию (+, -, *, /): ").strip()
        b = Decimal(input("Введите второе число: ").strip())
        result = calculate(a, operation, b)
    except DecimalException:
        print("Ошибка: некорректное число или переполнение", file=sys.stderr)
        return 2
    except (ValueError, ZeroDivisionError) as error:
        print("Ошибка: " + str(error), file=sys.stderr)
        return 2
    except (EOFError, KeyboardInterrupt):
        print("Ошибка: ввод прерван", file=sys.stderr)
        return 2
    print(f"Результат: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
