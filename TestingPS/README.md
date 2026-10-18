# Лабораторная работа №1

**Тема:** Составление тест-кейсов для готового кода. Качество ПО и место тестирования в жизненном цикле.

**Выполнил:** Василенко Илья, группа ПВ-231.  
**Ветка Git:** `Vasilenko_Ilya`.

## 1. Цель и задачи работы

**Цель:** получить практические навыки анализа бизнес-правил готового модуля, проектирования тест-кейсов и автоматизации проверок средствами `pytest`, а также оценить роль тестирования в обеспечении качества программного обеспечения.

В рамках работы необходимо изучить входные и выходные параметры, определить допустимые и недопустимые классы значений, составить позитивные, негативные и граничные тесты, запустить их и проанализировать покрытие и оставшиеся риски.

## 2. Анализ тестируемого модуля

**Объект тестирования:** функция `calculate_order_total` из файла [`order_total.py`](order_total.py), которая рассчитывает итоговую стоимость заказа.

### 2.1. Бизнес-правила

1. `item_price` — положительное число; нулевые, отрицательные и нечисловые значения недопустимы. `bool` также не допускается.
2. `quantity` — целое число в диапазоне от 1 до 100 включительно; `bool` не допускается.
3. `user_type` принимает только `regular` или `premium`.
4. `delivery_cost` — неотрицательное число; `bool` не допускается.
5. Для `premium` скидка составляет 10% **от суммы товаров**, но не от доставки.
6. Если сумма товаров **до скидки** не меньше 2000, стоимость доставки равна 0.
7. Итоговая сумма рассчитывается по формуле `subtotal - discount + delivery`.
8. Возвращаемый результат округляется до двух знаков после десятичной точки.

### 2.2. Входные и выходные параметры

| Параметр | Тип / допустимые значения | Недопустимые значения |
|---|---|---|
| `item_price` | `int` или `float`, строго больше 0 | 0, отрицательные, строки, `bool` |
| `quantity` | `int` от 1 до 100 | Меньше 1, больше 100, `float`, строки, `bool` |
| `user_type` | `regular` или `premium` | `vip`, другие значения |
| `delivery_cost` | `int` или `float`, от 0 | Отрицательные, строки, `bool` |

**Выходной параметр:** `total` — итоговая стоимость заказа типа `float`. При нарушении ограничений функция выбрасывает `ValueError`.

### 2.3. Границы и классы эквивалентности

- **Цена:** допустимые положительные числа; недопустимые ноль, отрицательные и значения неверного типа. Для проверки возле нуля выбрана цена `0.01` (это тестовое значение, а не установленный кодом минимальный шаг цены).
- **Количество:** допустимый интервал `[1, 100]`; недопустимые `0`, `101`, дробные и логические значения.
- **Порог бесплатной доставки:** проверены суммы `1999.99`, `2000` и `2000.01`.
- **Стоимость доставки:** ноль, положительная, отрицательная и значения неподходящего типа.
- **Тип пользователя:** `regular`, `premium` и недопустимый `vip`.
- **Premium:** отдельно проверены платная и бесплатная доставка, а также применение порога до скидки.

## 3. Тест-кейсы

**Общие предусловия:** Python и `pytest` установлены; модуль `order_total.py` доступен для импорта, функция вызывается непосредственно без внешних зависимостей.

**Шаги для каждого тест-кейса:** вызвать `calculate_order_total(item_price, quantity, user_type, delivery_cost)` с указанными данными; сравнить фактический результат с ожидаемым числом либо проверить тип и сообщение исключения.

В графе «Входные данные» значения идут в порядке `item_price, quantity, user_type, delivery_cost`.

| ID | Тип | Приоритет | Проверка | Входные данные | Ожидаемый результат |
|---|---|---|---|---|---|
| TC-01 | Позитивный | Высокий | Обычный заказ с доставкой | `500, 2, regular, 300` | `1300.00` |
| TC-02 | Позитивный | Средний | Нулевая стоимость доставки | `100, 1, regular, 0` | `100.00` |
| TC-03 | Позитивный | Высокий | Скидка premium и платная доставка | `1000, 1, premium, 300` | `1200.00` |
| TC-04 | Позитивный | Высокий | Скидка premium и бесплатная доставка | `2000, 1, premium, 300` | `1800.00` |
| TC-05 | Граничный | Высокий | Доставка при сумме ровно 2000 | `2000, 1, regular, 300` | `2000.00` |
| TC-06 | Граничный | Высокий | Сумма непосредственно ниже 2000 | `1999.99, 1, regular, 300` | `2299.99` |
| TC-07 | Граничный | Высокий | Сумма непосредственно выше 2000 | `2000.01, 1, regular, 300` | `2000.01` |
| TC-08 | Граничный | Средний | Минимальное допустимое количество | `20, 1, regular, 50` | `70.00` |
| TC-09 | Граничный | Средний | Максимальное допустимое количество | `10, 100, regular, 70` | `1070.00` |
| TC-10 | Граничный | Средний | Малая положительная цена | `0.01, 1, regular, 0` | `0.01` |
| TC-11 | Позитивный | Средний | Округление до двух знаков | `10.1234, 1, regular, 0` | `10.12` |
| TC-12 | Позитивный | Высокий | Порог доставки считается до скидки | `2050, 1, premium, 350` | `1845.00` |
| TC-13 | Негативный | Высокий | Нулевая цена | `0, 1, regular, 100` | `ValueError: item_price must be > 0` |
| TC-14 | Негативный | Средний | Отрицательная цена | `-1, 1, regular, 100` | `ValueError: item_price must be > 0` |
| TC-15 | Негативный | Средний | Цена задана строкой | `"100", 1, regular, 100` | `ValueError: item_price must be a number` |
| TC-16 | Негативный | Средний | Логическое значение цены | `True, 1, regular, 100` | `ValueError: item_price must be a number` |
| TC-17 | Негативный | Высокий | Нулевое количество | `100, 0, regular, 100` | `ValueError: quantity must be between 1 and 100` |
| TC-18 | Негативный | Высокий | Количество 101 | `100, 101, regular, 100` | `ValueError: quantity must be between 1 and 100` |
| TC-19 | Негативный | Средний | Дробное количество | `100, 1.5, regular, 100` | `ValueError: quantity must be an integer` |
| TC-20 | Негативный | Средний | Логическое значение количества | `100, True, regular, 100` | `ValueError: quantity must be an integer` |
| TC-21 | Негативный | Высокий | Недопустимый тип пользователя | `100, 1, vip, 100` | `ValueError: user_type must be 'regular' or 'premium'` |
| TC-22 | Негативный | Высокий | Отрицательная стоимость доставки | `100, 1, regular, -0.01` | `ValueError: delivery_cost must be >= 0` |
| TC-23 | Негативный | Средний | Стоимость доставки строкой | `100, 1, regular, "100"` | `ValueError: delivery_cost must be a number` |
| TC-24 | Негативный | Средний | Логическое значение доставки | `100, 1, regular, False` | `ValueError: delivery_cost must be a number` |

**Критерий успешности:** полученное число равно ожидаемому либо возникает `ValueError` с предусмотренным сообщением. Фактический результат всех 24 сценариев зафиксирован при запуске тестов ниже.

## 4. Реализация исходного кода

Файл [`order_total.py`](order_total.py):

```python
def calculate_order_total(item_price, quantity, user_type, delivery_cost):
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

## 5. Автоматизация тестирования

Файл [`test_order_total.py`](test_order_total.py):

```python
import pytest
from order_total import calculate_order_total


def test_tc01_regular_paid_delivery():
    assert calculate_order_total(500, 2, "regular", 300) == 1300.0


def test_tc02_regular_zero_delivery():
    assert calculate_order_total(100, 1, "regular", 0) == 100.0


def test_tc03_premium_paid_delivery():
    assert calculate_order_total(1000, 1, "premium", 300) == 1200.0


def test_tc04_premium_free_delivery():
    assert calculate_order_total(2000, 1, "premium", 300) == 1800.0


def test_tc05_free_delivery_at_threshold():
    assert calculate_order_total(2000, 1, "regular", 300) == 2000.0


def test_tc06_paid_delivery_below_threshold():
    assert calculate_order_total(1999.99, 1, "regular", 300) == 2299.99


def test_tc07_free_delivery_above_threshold():
    assert calculate_order_total(2000.01, 1, "regular", 300) == 2000.01


def test_tc08_minimum_quantity():
    assert calculate_order_total(20, 1, "regular", 50) == 70.0


def test_tc09_maximum_quantity():
    assert calculate_order_total(10, 100, "regular", 70) == 1070.0


def test_tc10_small_positive_price():
    assert calculate_order_total(0.01, 1, "regular", 0) == 0.01


def test_tc11_rounding_to_two_digits():
    assert calculate_order_total(10.1234, 1, "regular", 0) == 10.12


def test_tc12_free_delivery_uses_subtotal_before_discount():
    assert calculate_order_total(2050, 1, "premium", 350) == 1845.0


def test_tc13_zero_item_price():
    with pytest.raises(ValueError, match="item_price must be > 0"):
        calculate_order_total(0, 1, "regular", 100)


def test_tc14_negative_item_price():
    with pytest.raises(ValueError, match="item_price must be > 0"):
        calculate_order_total(-1, 1, "regular", 100)


def test_tc15_string_item_price():
    with pytest.raises(ValueError, match="item_price must be a number"):
        calculate_order_total("100", 1, "regular", 100)


def test_tc16_boolean_item_price():
    with pytest.raises(ValueError, match="item_price must be a number"):
        calculate_order_total(True, 1, "regular", 100)


def test_tc17_zero_quantity():
    with pytest.raises(ValueError, match="quantity must be between 1 and 100"):
        calculate_order_total(100, 0, "regular", 100)


def test_tc18_quantity_above_maximum():
    with pytest.raises(ValueError, match="quantity must be between 1 and 100"):
        calculate_order_total(100, 101, "regular", 100)


def test_tc19_non_integer_quantity():
    with pytest.raises(ValueError, match="quantity must be an integer"):
        calculate_order_total(100, 1.5, "regular", 100)


def test_tc20_boolean_quantity():
    with pytest.raises(ValueError, match="quantity must be an integer"):
        calculate_order_total(100, True, "regular", 100)


def test_tc21_invalid_user_type():
    with pytest.raises(ValueError, match="user_type must be"):
        calculate_order_total(100, 1, "vip", 100)


def test_tc22_negative_delivery_cost():
    with pytest.raises(ValueError, match="delivery_cost must be >= 0"):
        calculate_order_total(100, 1, "regular", -0.01)


def test_tc23_string_delivery_cost():
    with pytest.raises(ValueError, match="delivery_cost must be a number"):
        calculate_order_total(100, 1, "regular", "100")


def test_tc24_boolean_delivery_cost():
    with pytest.raises(ValueError, match="delivery_cost must be a number"):
        calculate_order_total(100, 1, "regular", False)
```

Каждому тест-кейсу соответствует отдельная тестовая функция с тем же номером `tc01`–`tc24`. В позитивных проверках используется `assert`; в негативных — `pytest.raises(ValueError, match=...)`, что позволяет проверить как возникновение ошибки, так и её сообщение.

## 6. Запуск и результаты

Установка зависимостей и запуск из каталога проекта:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

При подготовке работы проверка выполнена в среде Python 3.13.5, pytest 9.0.2:

```text
collected 24 items
TC-01 — TC-24: PASSED
24 passed in 0.09s
```

Подробный протокол запуска сохранён в файле [`pytest_results.txt`](pytest_results.txt). Все 24 теста завершились успешно; ошибок и пропусков нет.

Для оценки покрытия также была выполнена команда:

```bash
python -m pytest -q --cov=order_total --cov-branch --cov-report=term-missing
```

Результат измерения:

```text
Name             Stmts   Miss Branch BrPart  Cover
------------------------------------------------
order_total.py      20      0     14      0   100%
------------------------------------------------
TOTAL               20      0     14      0   100%
24 passed
```

Таким образом, **покрытие операторов и ветвей составляет 100%** для тестируемого файла `order_total.py`. Значение получено инструментом `pytest-cov`, а не определено приблизительно. Оно не означает полного отсутствия дефектов.

## 7. Анализ покрытия и оставшихся рисков

Тестами проверены обе альтернативы при валидации типов и диапазонов для `item_price`, `quantity` и `delivery_cost`, корректная и ошибочная ветви `user_type`, расчёт с премиальной скидкой и без неё, бесплатная и платная доставка, а также округление результата.

**Оставшиеся риски:**

1. Значения `float('nan')` и `float('inf')` не отвергаются существующей валидацией. Они могут приводить к некорректному результату, хотя обычные тест-кейсы проходят.
2. При денежных расчётах используется двоичная арифметика `float`. Для финансовой системы целесообразно отдельно согласовать правила округления и рассмотреть `Decimal`.
3. Не исследованы все варианты комбинаций невалидных аргументов и экстремально большие числа.
4. Покрытие 100% относится к ветвям данной функции и не заменяет интеграционные испытания, проверку внешних интерфейсов и тестирование производительности.

## 8. Вывод

В ходе лабораторной работы были выделены бизнес-правила, входные и выходные данные, граничные значения и классы эквивалентности модуля расчёта стоимости заказа. Разработаны **24 тест-кейса** (12 позитивных и граничных, 12 негативных) и реализованы соответствующие автотесты на `pytest`. Все проверки прошли успешно; измерено 100% покрытие операторов и ветвей исследуемого модуля.

Тестирование необходимо на протяжении жизненного цикла ПО: оно помогает уточнять требования, выявлять ошибки до релиза, подтверждать соблюдение бизнес-правил и предотвращать регрессии после изменений. Наличие успешно выполненных тестов повышает уверенность в качестве продукта, однако не устраняет необходимость дополнительных проверок на нестандартных данных и в реальных условиях эксплуатации.
