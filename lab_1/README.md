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

## Выполнил: Васильев Андрей ПВ-231

## Тестируемый модуль: расчёт стоимости заказа.

## Бизнес правила:

1. Цена товара должна быть больше 0.
2. Количество товара - целое число от 1 до 100 включительно.
3. Тип пользователя: **regular** или **premium**.
4. Стоимость доставки должны быть неотрицательной.
5. Для **premium**-пользователя даётся скидка 10% от суммы заказа.
6. Если сумма заказа до скидки >= 2000, доставка бесплатная.
7. Итоговая стоимость = сумма заказа - скидка + доставка.
8. Результат округляется до 2 знаком после запятой.

## Входные параметры:

1. item-price — цена одной единицы товара;
2. quantity — количество единиц;
3. user_type — тип пользователя;
4. delivery_cost — стоимость доставки.

## Выходной параметр:

1. total — итоговая стоимость заказа.

## Допустимые значения:

1. item_price > 0;
2. quantity — целое от 1 до 100;
3. user_type — regular или premium;
4. delivery_cost >= 0.

## Недопустимые значения:

1. item_price <= 0;
2. quantity <= 0, quantity > 100, нецелое число;
3. user_type не из списка;
4. delivery_cost < 0.

## Граничные значения:

1. item_price: 0, 0.01;
2. quantity: 1, 100, 101;
3. delivery_cost: 0, -0.01;
4. сумма заказа: 1999.99, 2000;
5. premium-скидка: проверяется отдельно.

## Код модуля:

```python
def calculate_order_total(item_price, quantity, user_type, delivery_cost):
    """
    Возвращает итоговую стоимость заказа.

    Бизнес-правила:
    - цена товара > 0;
    - количество: целое от 1 до 100;
    - user_type: 'regular' или 'premium';
    - delivery_cost >= 0;
    - premium-пользователь получает скидку 10%;
    - если сумма заказа >= 2000, доставка бесплатная.
    """
    if not isinstance(item_price, (int, float)) or isinstance(item_price, bool):
        raise ValueError("item_price must be a number")
    if item_price <= 0:
        raise ValueError("item_price must be > 0")

    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise ValueError("quantity must be an integer")
    if quantity < 1 or quantity > 100:
        raise ValueError("quantity must be between 1 and 100")

    if user_type not in ("regular", "premium"):
        raise ValueError("user_type must be 'regular' or 'premium'")

    if not isinstance(delivery_cost, (int, float)) or isinstance(delivery_cost, bool):
        raise ValueError("delivery_cost must be a number")
    if delivery_cost < 0:
        raise ValueError("delivery_cost must be >= 0")

    subtotal = item_price * quantity

    discount = subtotal * 0.10 if user_type == "premium" else 0.0
    total_after_discount = subtotal - discount

    delivery = 0.0 if subtotal >= 2000 else delivery_cost

    return round(total_after_discount + delivery, 2)
```

## Реализация автотестов:

```python
import pytest


# ---------- Позитивные тесты ----------

def test_regular_user_without_discount_and_paid_delivery():
    # TC-01. Обычный пользователь, платная доставка
    # Тип: позитивный. Приоритет: High.
    # Вход: price=500, qty=2, user=regular, delivery=300.
    # Ожидание: 500 * 2 + 300 = 1300.00 (без скидки, сумма < 2000)
    assert calculate_order_total(500, 2, "regular", 300) == 1300.0


def test_regular_user_with_zero_delivery():
    # TC-02. Обычный пользователь, доставка 0
    # Тип: позитивный. Приоритет: Medium.
    # Вход: price=100, qty=1, user=regular, delivery=0.
    # Ожидание: 100 * 1 + 0 = 100.00
    assert calculate_order_total(100, 1, "regular", 0) == 100.0


def test_premium_user_gets_discount():
    # TC-03. Premium-пользователь получает скидку
    # Тип: позитивный. Приоритет: High.
    # Вход: price=1000, qty=1, user=premium, delivery=300.
    # Ожидание: 1000 - 10% + 300 = 1200.00
    assert calculate_order_total(1000, 1, "premium", 300) == 1200.0


# ---------- Граничные тесты ----------

def test_min_price_boundary():
    # TC-04. Минимальная допустимая цена товара
    # Тип: граничный. Приоритет: Medium.
    # Вход: price=0.01, qty=1, user=regular, delivery=0.
    # Ожидание: 0.01 (нижняя граница item_price > 0)
    assert calculate_order_total(0.01, 1, "regular", 0) == 0.01


def test_max_quantity_boundary():
    # TC-05. Максимальное допустимое количество
    # Тип: граничный. Приоритет: Medium.
    # Вход: price=10, qty=100, user=regular, delivery=0.
    # Ожидание: 10 * 100 + 0 = 1000.00 (верхняя граница quantity = 100)
    assert calculate_order_total(10, 100, "regular", 0) == 1000.0


def test_free_delivery_at_2000_boundary():
    # TC-06. Бесплатная доставка при сумме ровно 2000
    # Тип: граничный. Приоритет: High.
    # Вход: price=2000, qty=1, user=regular, delivery=300.
    # Ожидание: 2000 + 0 = 2000.00 (доставка не добавляется, сумма >= 2000)
    assert calculate_order_total(2000, 1, "regular", 300) == 2000.0


def test_paid_delivery_just_below_2000_boundary():
    # TC-07. Платная доставка чуть ниже порога 2000
    # Тип: граничный. Приоритет: High.
    # Вход: price=1999.99, qty=1, user=regular, delivery=300.
    # Ожидание: 1999.99 + 300 = 2299.99 (сумма < 2000 — доставка платная)
    assert calculate_order_total(1999.99, 1, "regular", 300) == 2299.99


# ---------- Проверка скидки premium ----------

def test_premium_discount_with_paid_delivery():
    # TC-08. Premium-скидка при платной доставке
    # Тип: позитивный (проверка скидки). Приоритет: High.
    # Вход: price=500, qty=1, user=premium, delivery=300.
    # Ожидание: 500 - 50 + 300 = 750.00 (скидка 10% только на сумму заказа)
    assert calculate_order_total(500, 1, "premium", 300) == 750.0


def test_premium_discount_and_free_delivery():
    # TC-09. Premium-скидка + бесплатная доставка
    # Тип: позитивный (проверка скидки и доставки). Приоритет: High.
    # Вход: price=2000, qty=1, user=premium, delivery=300.
    # Ожидание: 2000 - 200 + 0 = 1800.00 (сумма >= 2000 — доставка бесплатная)
    assert calculate_order_total(2000, 1, "premium", 300) == 1800.0


# ---------- Негативные тесты ----------

def test_invalid_price_zero():
    # TC-10. Цена товара равна 0
    # Тип: негативный. Приоритет: High.
    # Вход: price=0, qty=1, user=regular, delivery=100.
    # Ожидание: ValueError (item_price должен быть > 0)
    with pytest.raises(ValueError):
        calculate_order_total(0, 1, "regular", 100)


def test_invalid_negative_price():
    # TC-11. Отрицательная цена товара
    # Тип: негативный. Приоритет: Medium.
    # Вход: price=-10, qty=1, user=regular, delivery=100.
    # Ожидание: ValueError (item_price должен быть > 0)
    with pytest.raises(ValueError):
        calculate_order_total(-10, 1, "regular", 100)


def test_invalid_quantity_zero():
    # TC-12. Количество товара равно 0
    # Тип: негативный. Приоритет: High.
    # Вход: price=100, qty=0, user=regular, delivery=100.
    # Ожидание: ValueError (quantity должен быть от 1 до 100)
    with pytest.raises(ValueError):
        calculate_order_total(100, 0, "regular", 100)


def test_invalid_quantity_too_large():
    # TC-13. Количество товара больше 100
    # Тип: негативный. Приоритет: Medium.
    # Вход: price=100, qty=101, user=regular, delivery=100.
    # Ожидание: ValueError (quantity должен быть от 1 до 100)
    with pytest.raises(ValueError):
        calculate_order_total(100, 101, "regular", 100)


def test_invalid_quantity_not_integer():
    # TC-14. Количество товара не целое
    # Тип: негативный. Приоритет: Medium.
    # Вход: price=100, qty=1.5, user=regular, delivery=100.
    # Ожидание: ValueError (quantity должен быть целым числом)
    with pytest.raises(ValueError):
        calculate_order_total(100, 1.5, "regular", 100)


def test_invalid_user_type():
    # TC-15. Неверный тип пользователя
    # Тип: негативный. Приоритет: High.
    # Вход: price=100, qty=1, user=vip, delivery=100.
    # Ожидание: ValueError (user_type должен быть regular или premium)
    with pytest.raises(ValueError):
        calculate_order_total(100, 1, "vip", 100)


def test_invalid_negative_delivery_cost():
    # TC-16. Отрицательная стоимость доставки
    # Тип: негативный. Приоритет: Medium.
    # Вход: price=100, qty=1, user=regular, delivery=-1.
    # Ожидание: ValueError (delivery_cost должен быть >= 0)
    with pytest.raises(ValueError):
        calculate_order_total(100, 1, "regular", -1)
```

## Результат тестирования:

```
============================= test session starts ==============================
collecting ... collected 16 items

Testing_lab1.py::test_regular_user_without_discount_and_paid_delivery PASSED [  6%]
Testing_lab1.py::test_regular_user_with_zero_delivery PASSED             [ 12%]
Testing_lab1.py::test_premium_user_gets_discount PASSED                  [ 18%]
Testing_lab1.py::test_min_price_boundary PASSED                          [ 25%]
Testing_lab1.py::test_max_quantity_boundary PASSED                       [ 31%]
Testing_lab1.py::test_free_delivery_at_2000_boundary PASSED              [ 37%]
Testing_lab1.py::test_paid_delivery_just_below_2000_boundary PASSED      [ 43%]
Testing_lab1.py::test_premium_discount_with_paid_delivery PASSED         [ 50%]
Testing_lab1.py::test_premium_discount_and_free_delivery PASSED          [ 56%]
Testing_lab1.py::test_invalid_price_zero PASSED                          [ 62%]
Testing_lab1.py::test_invalid_negative_price PASSED                      [ 68%]
Testing_lab1.py::test_invalid_quantity_zero PASSED                       [ 75%]
Testing_lab1.py::test_invalid_quantity_too_large PASSED                  [ 81%]
Testing_lab1.py::test_invalid_quantity_not_integer PASSED                [ 87%]
Testing_lab1.py::test_invalid_user_type PASSED                           [ 93%]
Testing_lab1.py::test_invalid_negative_delivery_cost PASSED              [100%]

============================== 16 passed in 0.03s ==============================

Process finished with exit code 0
```

## Вывод:

В ходе работы были проанализированы бизнес-правила модуля по расчёту стоимости заказа и составлено: 3 позитивных, 4 граничных, 2 на скидку premium-пользователям и 7 негативных. Тестами покрыты следующие ветки кода:

1. Валидация item_price.
2. Валидация quantity.
3. Валидация user_type.
4. Валидация delivery_cost.
5. Ветвь расчёта скидки.
6. Ветвь бесплатной доставки.
7. Ветвь расчёта итоговой суммы и округления.

Остаточные риски:

1. Не проверены значения чуть выше 2000 (2000.1).
2. Не проверены зачения boolean и NaN для item_price/quantity/delivery_cost.

Тестирование является важной часть жизненного цикла ПО, обеспечивающая:

1. Соответствие требованиям бизнеса.
2. Обнаружение дефектов на ранних этапах, когда их исправление не вызывает проблем.
3. Документирование поведения ПО.
4. Снижение вероятности ошибок, влияющих на клиентов.
5. Оценка готовности ПО к релизу.
