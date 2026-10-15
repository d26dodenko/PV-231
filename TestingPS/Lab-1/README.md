# Лабораторная работа №1 <br> Составление тест-кейсов для готового кода. Качество ПО и место тестирования в жизненном цикле

## Цель работы

Сформировать системное представление о качестве ПО и роли тестирования в жизненном цикле; приобрести практические навыки проектирования тест-кейсов и написания автотестов на основе готового кода.

**Задачи:**

1. Проанализировать готовый модуль и выделить бизнес-правила, входные и выходные данные, ограничения.
2. Составить набор тест-кейсов: позитивных, негативных, граничных, покрывающих эквивалентные классы.
3. Оформить тест-кейсы по стандартным атрибутам.
4. Реализовать автотесты на Python + pytest.
5. Запустить тесты и зафиксировать результаты.
6. Сделать вывод о связи тестирования, качества ПО и жизненного цикла.

## Задание:

1. Изучить исходный код и выписать все бизнес-правила.
2. Определить:
   - входные параметры;
   - выходной параметр;
   - допустимые и недопустимые значения;
   - граничные значения.
3. Составить **не менее 10 тест-кейсов**:
   - позитивные;
   - негативные;
   - граничные;
   - проверяющие скидку для premium-пользователей;
   - проверяющие бесплатную доставку.
4. Написать автотесты на `pytest`.
5. Запустить тесты командой `pytest -v`.
6. Сделать вывод: какие ветви кода покрыты, какие риски остались, почему тестирование важно для качества.

## Выполнил: Саввин Богдан ПВ-231

## Тестируемый модуль

Тестируется функция `calculate_baggage_fee` из файла `baggage_fee.py`.

Функция рассчитывает стоимость провоза багажа в зависимости от веса, типа рейса и наличия premium-статуса.

## Входные данные

- `weight_kg: float` — вес багажа в килограммах.
- `flight_type: str` — тип рейса: `domestic` или `international`.
- `is_premium: bool` — наличие premium-статуса.

## Выходные данные

- `float` — итоговая стоимость провоза багажа.
- `ValueError` — при недопустимых входных данных.

## Бизнес-правила

1. Если вес багажа меньше 0 кг, выбрасывается `ValueError`.
2. Если вес багажа больше 50 кг, выбрасывается `ValueError`.
3. Допустимые типы рейса: `domestic` и `international`.
4. Багаж весом до 10 кг включительно провозится бесплатно.
5. На внутреннем рейсе каждый килограмм сверх 10 кг стоит 150.
6. На международном рейсе каждый килограмм сверх 10 кг стоит 250.
7. Если вес багажа больше 30 кг, добавляется фиксированный сбор 1000.
8. Premium-пассажир получает скидку 30% на итоговую стоимость.
9. Итоговая сумма округляется до двух знаков после запятой.

## Допустимые и недопустимые значения

### weight_kg

Допустимые значения: от 0 до 50 включительно.

Недопустимые значения:
- меньше 0;
- больше 50.

### flight_type

Допустимые значения:
- `domestic`;
- `international`.

Недопустимые значения:
- любые другие строки.

### is_premium

Допустимые значения:
- `True`;
- `False`.

## Классы эквивалентности

Для `weight_kg`:

- `< 0` — недопустимый класс;
- `[0, 10]` — бесплатный багаж;
- `(10, 30]` — платный багаж без дополнительного сбора;
- `(30, 50]` — платный багаж с дополнительным сбором;
- `> 50` — недопустимый класс.

Для `flight_type`:

- `domestic`;
- `international`;
- недопустимое значение.

Для `is_premium`:

- premium;
- обычный пассажир.

## Граничные значения

Для параметра `weight_kg` выделены следующие границы:

- минимально допустимый вес `0 кг`: `-0.01`, `0`, `0.01`;
- граница бесплатного багажа `10 кг`: `9.99`, `10`, `10.01`;
- граница дополнительного сбора `30 кг`: `29.99`, `30`, `30.01`;
- максимально допустимый вес `50 кг`: `49.99`, `50`, `50.01`.
## Тест-кейсы

Предусловие для всех тест-кейсов: функция `calculate_baggage_fee` доступна для вызова, используются тарифы и ограничения, указанные в бизнес-правилах.

Шаги для позитивных и граничных тест-кейсов:
1. Вызвать `calculate_baggage_fee` с указанными входными данными.
2. Сравнить фактический результат с ожидаемым.

Шаги для негативных тест-кейсов:
1. Вызвать `calculate_baggage_fee` с недопустимыми входными данными.
2. Проверить, что выбрасывается `ValueError`.

В выбранном модуле аналогом проверки бесплатной доставки является бесплатный провоз багажа весом до `10 кг` включительно.

| ID | Название | Тип | Входные данные | Ожидаемый результат |
|---|---|---|---|---|
| TC-01 | Нулевой вес багажа | граничный | 0 кг, domestic, обычный | 0.00 |
| TC-02 | Верхняя граница бесплатного багажа | граничный | 10 кг, domestic, обычный | 0.00 |
| TC-03 | Первый платный вес | граничный | 10.01 кг, domestic, обычный | 1.50 |
| TC-04 | Обычный багаж на внутреннем рейсе | позитивный | 20 кг, domestic, обычный | 1500.00 |
| TC-05 | Обычный багаж на международном рейсе | позитивный | 20 кг, international, обычный | 2500.00 |
| TC-06 | Верхняя граница без сбора за тяжёлый багаж | граничный | 30 кг, domestic, обычный | 3000.00 |
| TC-07 | Первый вес с дополнительным сбором | граничный | 30.01 кг, domestic, обычный | 4001.50 |
| TC-08 | Тяжёлый багаж на международном рейсе | позитивный | 31 кг, international, обычный | 6250.00 |
| TC-09 | Максимально допустимый вес | граничный | 50 кг, domestic, обычный | 7000.00 |
| TC-10 | Premium-скидка на обычный багаж | позитивный | 20 кг, domestic, premium | 1050.00 |
| TC-11 | Premium-скидка на тяжёлый багаж | позитивный | 31 кг, domestic, premium | 2905.00 |
| TC-12 | Бесплатный багаж для premium-пассажира | позитивный | 10 кг, international, premium | 0.00 |
| TC-13 | Вес ниже минимальной границы | негативный | -0.01 кг, domestic, обычный | ValueError |
| TC-14 | Вес выше максимально допустимого | негативный | 50.01 кг, domestic, обычный | ValueError |
| TC-15 | Некорректный тип рейса | негативный | 20 кг, space, обычный | ValueError |

## Исходный код

Файл `baggage_fee.py`:

```python
def calculate_baggage_fee(
    weight_kg: float,
    flight_type: str,
    is_premium: bool = False
) -> float:
    if weight_kg < 0:
        raise ValueError("weight_kg must be >= 0")

    if weight_kg > 50:
        raise ValueError("weight_kg must be <= 50")

    if flight_type not in ("domestic", "international"):
        raise ValueError("invalid flight_type")

    if weight_kg <= 10:
        cost = 0.0
    elif flight_type == "domestic":
        cost = (weight_kg - 10) * 150
    else:
        cost = (weight_kg - 10) * 250

    if weight_kg > 30:
        cost += 1000

    if is_premium:
        cost *= 0.7

    return round(cost, 2)
```

## Реализация автотестов

Файл `tests/test_baggage_fee.py`:

```python
import pytest

from baggage_fee import calculate_baggage_fee


def test_zero_weight():
    # TC-01. Нулевой вес багажа
    # Тип: граничный.
    # Вход: weight=0, flight=domestic, premium=False.
    # Ожидание: багаж до 10 кг бесплатный, стоимость = 0.00.
    assert calculate_baggage_fee(0, "domestic", False) == 0.0


def test_free_baggage_limit():
    # TC-02. Верхняя граница бесплатного багажа
    # Тип: граничный.
    # Вход: weight=10, flight=domestic, premium=False.
    # Ожидание: 10 кг включительно провозятся бесплатно, стоимость = 0.00.
    assert calculate_baggage_fee(10, "domestic", False) == 0.0


def test_first_paid_weight():
    # TC-03. Вес немного выше бесплатного лимита
    # Тип: граничный.
    # Вход: weight=10.01, flight=domestic, premium=False.
    # Ожидание: (10.01 - 10) * 150 = 1.50.
    assert calculate_baggage_fee(10.01, "domestic", False) == 1.5


def test_domestic_flight():
    # TC-04. Обычный багаж на внутреннем рейсе
    # Тип: позитивный.
    # Вход: weight=20, flight=domestic, premium=False.
    # Ожидание: (20 - 10) * 150 = 1500.00.
    assert calculate_baggage_fee(20, "domestic", False) == 1500.0


def test_international_flight():
    # TC-05. Обычный багаж на международном рейсе
    # Тип: позитивный.
    # Вход: weight=20, flight=international, premium=False.
    # Ожидание: (20 - 10) * 250 = 2500.00.
    assert calculate_baggage_fee(20, "international", False) == 2500.0


def test_heavy_baggage_boundary():
    # TC-06. Верхняя граница без сбора за тяжёлый багаж
    # Тип: граничный.
    # Вход: weight=30, flight=domestic, premium=False.
    # Ожидание: (30 - 10) * 150 = 3000.00, дополнительного сбора нет.
    assert calculate_baggage_fee(30, "domestic", False) == 3000.0


def test_heavy_baggage_fee():
    # TC-07. Первый вес с дополнительным сбором
    # Тип: граничный.
    # Вход: weight=30.01, flight=domestic, premium=False.
    # Ожидание: (30.01 - 10) * 150 + 1000 = 4001.50.
    assert calculate_baggage_fee(30.01, "domestic", False) == 4001.5


def test_heavy_baggage_international():
    # TC-08. Тяжёлый багаж на международном рейсе
    # Тип: позитивный.
    # Вход: weight=31, flight=international, premium=False.
    # Ожидание: (31 - 10) * 250 + 1000 = 6250.00.
    assert calculate_baggage_fee(31, "international", False) == 6250.0


def test_maximum_weight():
    # TC-09. Максимально допустимый вес
    # Тип: граничный.
    # Вход: weight=50, flight=domestic, premium=False.
    # Ожидание: (50 - 10) * 150 + 1000 = 7000.00.
    assert calculate_baggage_fee(50, "domestic", False) == 7000.0


def test_premium_discount():
    # TC-10. Premium-скидка на обычный багаж
    # Тип: позитивный.
    # Вход: weight=20, flight=domestic, premium=True.
    # Ожидание: ((20 - 10) * 150) * 0.7 = 1050.00.
    assert calculate_baggage_fee(20, "domestic", True) == 1050.0


def test_premium_with_heavy_baggage():
    # TC-11. Premium-скидка на тяжёлый багаж
    # Тип: позитивный.
    # Вход: weight=31, flight=domestic, premium=True.
    # Ожидание: ((31 - 10) * 150 + 1000) * 0.7 = 2905.00.
    assert calculate_baggage_fee(31, "domestic", True) == 2905.0


def test_free_baggage_for_premium():
    # TC-12. Бесплатный багаж для premium-пассажира
    # Тип: позитивный.
    # Вход: weight=10, flight=international, premium=True.
    # Ожидание: багаж до 10 кг бесплатный, стоимость после скидки остаётся 0.00.
    assert calculate_baggage_fee(10, "international", True) == 0.0


def test_negative_weight():
    # TC-13. Вес ниже минимальной границы
    # Тип: негативный.
    # Вход: weight=-0.01, flight=domestic, premium=False.
    # Ожидание: ValueError, так как вес не может быть меньше 0.
    with pytest.raises(ValueError):
        calculate_baggage_fee(-0.01, "domestic", False)


def test_weight_over_limit():
    # TC-14. Вес выше максимально допустимого
    # Тип: негативный.
    # Вход: weight=50.01, flight=domestic, premium=False.
    # Ожидание: ValueError, так как вес больше 50 кг.
    with pytest.raises(ValueError):
        calculate_baggage_fee(50.01, "domestic", False)


def test_invalid_flight_type():
    # TC-15. Некорректный тип рейса
    # Тип: негативный.
    # Вход: weight=20, flight=space, premium=False.
    # Ожидание: ValueError, так как допустимы только domestic и international.
    with pytest.raises(ValueError):
        calculate_baggage_fee(20, "space", False)
```

## Запуск тестов

```text
babadzaki@fedora:~/probe/testing/lab1_baggage$ pytest -v
======================================================================================== test session starts =========================================================================================
platform linux -- Python 3.14.6, pytest-8.4.2, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/babadzaki/probe/testing/lab1_baggage
configfile: pytest.ini
plugins: anyio-4.13.0
collected 15 items

tests/test_baggage_fee.py::test_zero_weight PASSED                                                                                                                           [  6%]
tests/test_baggage_fee.py::test_free_baggage_limit PASSED                                                                                                                    [ 13%]
tests/test_baggage_fee.py::test_first_paid_weight PASSED                                                                                                                     [ 20%]
tests/test_baggage_fee.py::test_domestic_flight PASSED                                                                                                                       [ 26%]
tests/test_baggage_fee.py::test_international_flight PASSED                                                                                                                  [ 33%]
tests/test_baggage_fee.py::test_heavy_baggage_boundary PASSED                                                                                                                [ 40%]
tests/test_baggage_fee.py::test_heavy_baggage_fee PASSED                                                                                                                     [ 46%]
tests/test_baggage_fee.py::test_heavy_baggage_international PASSED                                                                                                           [ 53%]
tests/test_baggage_fee.py::test_maximum_weight PASSED                                                                                                                        [ 60%]
tests/test_baggage_fee.py::test_premium_discount PASSED                                                                                                                      [ 66%]
tests/test_baggage_fee.py::test_premium_with_heavy_baggage PASSED                                                                                                            [ 73%]
tests/test_baggage_fee.py::test_free_baggage_for_premium PASSED                                                                                                              [ 80%]
tests/test_baggage_fee.py::test_negative_weight PASSED                                                                                                                       [ 86%]
tests/test_baggage_fee.py::test_weight_over_limit PASSED                                                                                                                     [ 93%]
tests/test_baggage_fee.py::test_invalid_flight_type PASSED                                                                                                                   [100%]

========================================================================================= 15 passed in 0.02s =========================================================================================
```
## Вывод

В ходе лабораторной работы были выделены бизнес-правила тестируемой функции, определены входные и выходные данные, классы эквивалентности и граничные значения. Были составлены позитивные, негативные и граничные тест-кейсы и реализованы автотесты с использованием pytest.

### Покрытые ветви

Автотесты проверяют:

- нижнюю и верхнюю границы веса;
- бесплатный багаж;
- внутренний и международный рейс;
- обычную тарификацию;
- дополнительный сбор за тяжёлый багаж;
- premium-скидку;
- комбинацию premium-скидки с дополнительным сбором;
- недопустимый вес;
- недопустимый тип рейса.

### Оставшиеся риски

- функция явно не проверяет тип `weight_kg`;
- функция явно не проверяет тип `is_premium`;
- не определено поведение для специальных категорий багажа;
- не учитываются дополнительные тарифы конкретных авиакомпаний;
- дробный вес рассчитывается пропорционально, хотя в реальной системе правила округления могут отличаться.
