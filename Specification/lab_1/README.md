# Лабораторная работа

**Тема:** Критерии качества ПО: сложность, корректность, надёжность, трудоёмкость. Оценка качества ПО.

**Цель:** Освоить практические методы оценки качества и метрик программного обеспечения.

## Задания

### Часть 1. Теоретическая

1. Опишите 3 наиболее значимые проблемы, возникающие при разработке сложных программных систем.
2. Составьте таблицу: «Проблема → Возможное решение → Инструменты/методы».

### Часть 2. Практическая

1. Создайте тестовый проект на Python (например, калькулятор).
2. Создайте задачи для проекта в Аспро (или другой системе трекинга).
3. Покройте код тестами (Unit tests).
4. Зафиксируйте покрытие тестами кода (например, с помощью coverage.py).
5. Возьмите небольшой программный проект (учебное консольное приложение или открытый код с GitHub).
6. Определите размер ПО (LOC).
7. Рассчитайте цикломатическую сложность одной из функций (можно использовать `radon cc -s calculator`).
8. Оцените дефектность (если есть баг-репорты или замечания).
9. Составьте итоговую таблицу метрик проекта, включающую:
   - размер (LOC),
   - сложность (цикломатическая),
   - качество (дефекты),
   - время реакции (если есть возможность),
   - процент покрытия тестами.

## Напоминание формулы цикломатической сложности

\[
V(G) = E - N + 2P
\]

где:

- \(E\) — количество рёбер графа потока управления,
- \(N\) — количество узлов (блоков кода),
- \(P\) — количество компонент (обычно = 1).

Более простое правило:

\[
V(G) = \text{количество условий} + 1
\]

## Пример функции на Python

```python
def classify_number(x):
    if x > 0:
        print("Positive")
    elif x == 0:
        print("Zero")
    else:
        print("Negative")
```

**Анализ:** В функции есть одно ветвление `if - elif - else`, которое образует 3 возможных пути выполнения. Условий проверки = 2 (`x > 0` и `x == 0`).

Расчёт через условия:

\[
V(G) = 2 + 1 = 3
\]

Расчёт через граф потока: Узлы (N): 4, Рёбра (E): 5, Компонент (P): 1.

\[
V(G) = 5 - 4 + 2 \times 1 = 3
\]

## Выполнение

### Выполнил: Васильев А. А. ПВ-231

### Часть 1

3 наиболее значимые проблемы:

1. Архитектурная сложность — по мере развития системы количество модулей, интеграций и зависимостей растёт нелинейно, из-за чего изменения в одном месте непредсказуемо влияет на другие, а систему становится трудно понимать и сопровождать.

2. Обеспечение качества и тестируемость — сложные системы имеют множество сценариев, состояний и внешних интеграций; полное покрытие тестами дорого, а дефекты проявляются на поздних этапах, когда исправление стоит на порядок дороже.

3. Управление требованиями и коммуникация в распределённой команде — размытые или меняющиеся требования, разнородные команды и подрядчики приводят к несоответствию ожиданий и результата, дублированию работы и накоплению технического долга.

Таблица <<Проблема -> Возможное решение -> Инструменты/методы>>:

| Проблема | Возможное решение | Инструменты/методы |
|---|---|---|
| Архитектурная сложность | Модульная/слабо связанная архитектура, чёткие границы сервисов, регулярный рефакторинг, контроль зависимостей | Доменно-ориентированное проектирование, микросервисы/модульный монолит, статический анализ зависимостей, код-ревью |
| Обеспечение качества и тестируемость | Многоуровневая пирамида тестов, автоматизация регрессии и CI/CD | Юнит/интеграционные-тесты, тест-менеджмент, CI/CD, покрытие, нагрузочное тестирование |
| Управление требованиями и коммуникация в команде | Итеративная разработка с частой обратной связью, единый источник требований, прозрачные процессы | Agile/Scrum, Kanban, User Stories, трекеры, документация, регулярные демо и ретроспективы |

### Часть 2

### Код калькулятора:

```python
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b


def power(base, exponent):
    if exponent < 0:
        if base == 0:
            raise ValueError("Ноль нельзя возводить в отрицательную степень")
        return 1 / (base ** abs(exponent))
    elif exponent == 0:
        return 1
    else:
        result = 1
        for _ in range(exponent):
            result *= base
        return result


def main():
    operations = {
        "1": ("Сложение", add),
        "2": ("Вычитание", subtract),
        "3": ("Умножение", multiply),
        "4": ("Деление", divide),
        "5": ("Степень", power),
    }

    print("Доступные операции:")
    for key, (name, _) in operations.items():
        print(f"  {key}. {name}")

    choice = input("Выберите операцию (1-5): ").strip()
    if choice not in operations:
        print("Неверный выбор")
        return

    try:
        a = float(input("Введите первое число: "))
        b = float(input("Введите второе число: "))
        name, func = operations[choice]
        print(f"Результат ({name}): {func(a, b)}")
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
```

### Список тестов:

Для функции сложения:

1. test_add_positive -- проверяет сложение двух положительных чисел.

2. test_add_negative -- проверяет сложение двух отрицательных чисел.

3. test_add_zero -- проверяет сложение с нулём.

Для функции вычитания:

1. test_subtract_positive -- обычное вычитание, где результат положительный.

2. test_subtract_negative_result -- вычитание, где результат отрицательный.

Для функции умножения:

1. test_multiply_positive -- умножение двух положительных чисел.

2. test_multiply_by_zero -- умножение на ноль.

3. test_multiply_negative -- умножение положительного на отрицательное.

Для функции деления:

1. test_divide_positive -- деление без остатка.

2. test_divide_float -- деление с дробным результатом.

3. test_divide_by_zero_raises -- деление на ноль.

Для функции возведения в степень:

1. test_power_positive -- возведение в положительную степень.

2. test_power_zero_exponent -- возведение в нулевую степень.

3. test_power_negative_exponent -- возведение в отрицательную степень.

4. test_power_zero_negative_raises -- возведение нуля в отрицательную степень.

### Код unit-тестов:

```python
import pytest

from Specification_1 import add, subtract, multiply, divide, power


# ---------- Сложение ----------
def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-2, -3) == -5


def test_add_zero():
    assert add(0, 5) == 5


# ---------- Вычитание ----------
def test_subtract_positive():
    assert subtract(10, 4) == 6


def test_subtract_negative_result():
    assert subtract(3, 10) == -7


# ---------- Умножение ----------
def test_multiply_positive():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(7, 0) == 0


def test_multiply_negative():
    assert multiply(-2, 5) == -10


# ---------- Деление ----------
def test_divide_positive():
    assert divide(10, 2) == 5


def test_divide_float():
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Деление на ноль"):
        divide(1, 0)


# ---------- Степень ----------
def test_power_positive():
    assert power(2, 3) == 8


def test_power_zero_exponent():
    assert power(5, 0) == 1


def test_power_negative_exponent():
    assert power(2, -2) == 0.25


def test_power_zero_negative_raises():
    with pytest.raises(ValueError, match="отрицательную степень"):
        power(0, -1)
```

### Результат выполнения тестов:

```
============================= test session starts ==============================
collecting ... collected 15 items

coverage.py::test_add_positive PASSED                                    [  6%]
coverage.py::test_add_negative PASSED                                    [ 13%]
coverage.py::test_add_zero PASSED                                        [ 20%]
coverage.py::test_subtract_positive PASSED                               [ 26%]
coverage.py::test_subtract_negative_result PASSED                        [ 33%]
coverage.py::test_multiply_positive PASSED                               [ 40%]
coverage.py::test_multiply_by_zero PASSED                                [ 46%]
coverage.py::test_multiply_negative PASSED                               [ 53%]
coverage.py::test_divide_positive PASSED                                 [ 60%]
coverage.py::test_divide_float PASSED                                    [ 66%]
coverage.py::test_divide_by_zero_raises PASSED                           [ 73%]
coverage.py::test_power_positive PASSED                                  [ 80%]
coverage.py::test_power_zero_exponent PASSED                             [ 86%]
coverage.py::test_power_negative_exponent PASSED                         [ 93%]
coverage.py::test_power_zero_negative_raises PASSED                      [100%]

============================== 15 passed in 0.03s ==============================
```

### Вычисление метрик

LOC = 46

Цикломатическая сложность (через radon) = 2.33:
```
Specification_1.py
    F 19:0 power - A (5)
    F 33:0 main - A (4)
    F 13:0 divide - A (2)
    F 1:0 add - A (1)
    F 5:0 subtract - A (1)
    F 9:0 multiply - A (1)

6 blocks (classes, functions, methods) analyzed.
Average complexity: A (2.3333333333333335)
```

### Итоговая таблица результатов:

| Метрика | Значение |
|---|---|
| Размер ПО (LOC) | 46 физических строк |
| Цикломатическая сложность | средняя по файлу = 2.33 (A) |
| Качество (дефекты) | 0 дефектов выявлено |
| Время реакции | ≈ 1 час от создания задачи до её закрытия |
| Процент покрытия тестами | ≈ 92% (т.к. не тестировалась функция main) |
