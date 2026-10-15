# Лабораторная работа 1

## Тема

Составление тест-кейсов для готового кода. Качество ПО и место тестирования в жизненном цикле

## Цель работы

Сформировать представление о качестве ПО и роли тестирования в жизненном цикле программы. Научиться анализировать бизнес-правила готового кода, составлять тест-кейсы и выполнять автоматическое тестирование с помощью `pytest`.

## Выполнил: Калашников Егор Олегович, ПВ-231

## Тестируемый модуль: расчёт стоимости доставки книг

## Бизнес-правила:

1. Сумма заказа (`order_amount`) должна быть числом не меньше 0.
2. Вес посылки (`weight_kg`) должен быть числом больше 0.
3. Статус покупателя (`is_premium`) может принимать только `True` или `False`.
4. Если сумма заказа 3500 рублей или больше, доставка бесплатная.
5. Если сумма заказа меньше 3500 рублей, стоимость зависит от веса:
   - вес до 2 кг включительно — 180 рублей;
   - вес больше 2, но не больше 5 кг — 280 рублей;
   - вес больше 5 кг — 280 рублей + 50 рублей за каждый дополнительный кг.
6. Для премиум покупателя действует скидка 25% на стоимость платной доставки.
7. Если доставка бесплатная, премиум скидка не изменяет её стоимость.
8. Результат округляется до двух знаков после запятой.
9. Если параметр имеет неправильный тип, вызывается `TypeError`. Если сумма заказа отрицательная или вес меньше либо равен 0 — `ValueError`.

## Входные параметры:

1. `order_amount` — сумма заказа в рублях
2. `weight_kg` — вес посылки в килограммах
3. `is_premium` — наличие премиума у покупателя

## Выходной параметр:

1. `delivery_cost` — рассчитанная стоимость доставки в рублях

## Допустимые значения:

1. `order_amount` — число, `>= 0`;
2. `weight_kg` — число, `> 0`;
3. `is_premium` — `True` или `False`.

## Недопустимые значения:

1. `order_amount` — отрицательное число, строка, `None`, `bool` и др.
2. `weight_kg` — 0, отрицательное число, строка, `None`, `bool` и др.
3. `is_premium` — строка, число, `None` и др.

## Граничные значения:

1. `order_amount`: `-0.01`, `0`, `3499.99`, `3500`;
2. `weight_kg`: `0`, `2`, `2.01`, `5`, `6.5`;
3. `is_premium`: `False`, `True`;
4. Стоимость доставки: переход от платной к бесплатной при сумме заказа 3500 рублей.

## Код модуля:

```python
def calculate_book_delivery(order_amount: float, weight_kg: float, is_premium: bool) -> float:
    if type(order_amount) not in (int, float):
        raise TypeError("order_amount must be a number")
    if type(weight_kg) not in (int, float):
        raise TypeError("weight_kg must be a number")
    if type(is_premium) is not bool:
        raise TypeError("is_premium must be a boolean")

    if order_amount < 0:
        raise ValueError("order_amount must be non-negative")
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")

    if order_amount >= 3500:
        return 0.0

    if weight_kg <= 2:
        cost = 180.0
    elif weight_kg <= 5:
        cost = 280.0
    else:
        cost = 280.0 + (weight_kg - 5) * 50.0

    if is_premium:
        cost *= 0.75

    return round(cost, 2)
```

## Составленные тест-кейсы:

| № | Тест-кейс | Тип | Приоритет | Входные данные `(order_amount, weight_kg, is_premium)` | Ожидаемый результат |
| --- | --- | --- | --- | --- | --- |
| 1 | Обычный заказ, лёгкая посылка | Позитивный | Medium | `(1000, 1, False)` | `180.0` |
| 2 | Вес ровно 2 кг | Граничный | High | `(1000, 2, False)` | `180.0` |
| 3 | Вес чуть больше 2 кг | Граничный | High | `(1000, 2.01, False)` | `280.0` |
| 4 | Вес ровно 5 кг | Граничный | High | `(1000, 5, False)` | `280.0` |
| 5 | Доплата за вес свыше 5 кг | Позитивный | High | `(1000, 6.5, False)` | `355.0` |
| 6 | До бесплатной доставки не хватает 1 копейки | Граничный | High | `(3499.99, 4, False)` | `280.0` |
| 7 | Бесплатная доставка от 3500 рублей | Граничный | High | `(3500, 4, False)` | `0.0` |
| 8 | Premium-скидка для тяжёлой посылки | Позитивный, premium | High | `(1000, 6.5, True)` | `266.25` |
| 9 | Premium и бесплатная доставка | Позитивный, premium | High | `(3500, 6.5, True)` | `0.0` |
| 10 | Отрицательная сумма заказа | Негативный | High | `(-0.01, 1, False)` | `ValueError` |
| 11 | Вес равен нулю | Негативный, граничный | High | `(1000, 0, False)` | `ValueError` |
| 12 | Сумма заказа — строка | Негативный | Medium | `("1000", 1, False)` | `TypeError` |
| 13 | Вес — строка | Негативный | Medium | `(1000, "1", False)` | `TypeError` |
| 14 | Premium-статус задан строкой | Негативный | Medium | `(1000, 1, "yes")` | `TypeError` |

## Реализация автотестов:
```python
import pytest

from delivery import calculate_book_delivery


def test_regular_light_parcel():
    """обычный заказ, вес в первом тарифе"""
    assert calculate_book_delivery(1000, 1, False) == 180.0


def test_weight_2_kg_boundary():
    """верхняя граница первого тарифа"""
    assert calculate_book_delivery(1000, 2, False) == 180.0


def test_weight_just_above_2_kg():
    """сразу после первого порога действует второй тариф"""
    assert calculate_book_delivery(1000, 2.01, False) == 280.0


def test_weight_5_kg_boundary():
    """верхняя граница второго тарифа"""
    assert calculate_book_delivery(1000, 5, False) == 280.0


def test_heavy_parcel_extra_charge():
    """доплата за вес свыше 5 кг"""
    assert calculate_book_delivery(1000, 6.5, False) == 355.0


def test_order_just_below_free_threshold():
    """на 1 копейку меньше порога бесплатной доставки"""
    assert calculate_book_delivery(3499.99, 4, False) == 280.0


def test_order_at_free_threshold():
    """на пороге 3500 рублей доставка бесплатная"""
    assert calculate_book_delivery(3500, 4, False) == 0.0


def test_premium_discount_for_heavy_parcel():
    """premium уменьшает платную доставку на 25%"""
    assert calculate_book_delivery(1000, 6.5, True) == 266.25


def test_premium_does_not_change_free_delivery():
    """premium и бесплатная доставка совместимы"""
    assert calculate_book_delivery(3500, 6.5, True) == 0.0


def test_negative_order_amount():
    """отрицательная сумма заказа запрещена"""
    with pytest.raises(ValueError, match="order_amount must be non-negative"):
        calculate_book_delivery(-0.01, 1, False)


def test_zero_weight():
    """нулевой вес недопустим"""
    with pytest.raises(ValueError, match="weight_kg must be positive"):
        calculate_book_delivery(1000, 0, False)


def test_string_order_amount():
    """сумма заказа должна быть числом"""
    with pytest.raises(TypeError, match="order_amount must be a number"):
        calculate_book_delivery("1000", 1, False)


def test_string_weight():
    """вес посылки должен быть числом"""
    with pytest.raises(TypeError, match="weight_kg must be a number"):
        calculate_book_delivery(1000, "1", False)


def test_invalid_premium_flag():
    """флаг premium должен быть bool, а не строкой"""
    with pytest.raises(TypeError, match="is_premium must be a boolean"):
        calculate_book_delivery(1000, 1, "yes")
```

## Результаты тестирования:
```text
collecting ... collected 14 items

test_delivery.py::test_regular_light_parcel PASSED 					       [  7%]
test_delivery.py::test_weight_2_kg_boundary PASSED               		   [ 14%]
test_delivery.py::test_weight_just_above_2_kg PASSED             		   [ 21%]
test_delivery.py::test_weight_5_kg_boundary PASSED               		   [ 28%]
test_delivery.py::test_heavy_parcel_extra_charge PASSED          		   [ 35%]
test_delivery.py::test_order_just_below_free_threshold PASSED    		   [ 42%]
test_delivery.py::test_order_at_free_threshold PASSED            		   [ 50%]
test_delivery.py::test_premium_discount_for_heavy_parcel PASSED  		   [ 57%]
test_delivery.py::test_premium_does_not_change_free_delivery PASSED        [ 64%]
test_delivery.py::test_negative_order_amount PASSED                        [ 71%]
test_delivery.py::test_zero_weight PASSED                                  [ 78%]
test_delivery.py::test_string_order_amount PASSED                          [ 85%]
test_delivery.py::test_string_weight PASSED                                [ 92%]
test_delivery.py::test_invalid_premium_flag PASSED                         [100%]

=============================== 14 passed in 0.04s ==============================
```

## Вывод:

В ходе выполнения лабораторной работы была разработана и проанализирована функция расчёта доставки книг. Выделены бизнес-правила, входные и выходные параметры, допустимые и недопустимые значения, определены основные граничные случаи.

Составлено 14 тест-кейсов: позитивные, негативные и граничные проверки; некоторые кейсы относятся сразу к нескольким категориям. Отдельно проверены premium-скидка и бесплатная доставка. Реализованы 14 автоматических тестов на `pytest`, все они успешно пройдены.

Тестами проверены валидация параметров, все тарифы доставки, переход на бесплатную доставку при 3500 рублях и скидка premium-пользователей.

При этом остаются риски, не проверенные в данной работе: передача `NaN` и бесконечностей, очень большие значения веса и суммы заказа, а также особенности округления для необычных дробных значений.

Тестирование важно на разных этапах жизненного цикла ПО. Оно позволяет находить ошибки в бизнес-логике на этапе разработки, подтверждать корректность перед выпуском и повторно проверять работу программы после изменения тарифов или правил расчёта.
