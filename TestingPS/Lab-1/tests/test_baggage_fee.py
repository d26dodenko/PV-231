import pytest

from baggage_fee import calculate_baggage_fee


def test_zero_weight():
    # TC-01. Нулевой вес багажа
    # Тип: граничный. Приоритет: High.
    # Вход: weight=0, flight=domestic, premium=False.
    # Ожидание: багаж до 10 кг бесплатный, стоимость = 0.00.
    assert calculate_baggage_fee(0, "domestic", False) == 0.0


def test_free_baggage_limit():
    # TC-02. Верхняя граница бесплатного багажа
    # Тип: граничный. Приоритет: High.
    # Вход: weight=10, flight=domestic, premium=False.
    # Ожидание: 10 кг включительно провозятся бесплатно, стоимость = 0.00.
    assert calculate_baggage_fee(10, "domestic", False) == 0.0


def test_first_paid_weight():
    # TC-03. Вес немного выше бесплатного лимита
    # Тип: граничный. Приоритет: High.
    # Вход: weight=10.01, flight=domestic, premium=False.
    # Ожидание: (10.01 - 10) * 150 = 1.50.
    assert calculate_baggage_fee(10.01, "domestic", False) == 1.5


def test_domestic_flight():
    # TC-04. Обычный багаж на внутреннем рейсе
    # Тип: позитивный. Приоритет: Medium.
    # Вход: weight=20, flight=domestic, premium=False.
    # Ожидание: (20 - 10) * 150 = 1500.00.
    assert calculate_baggage_fee(20, "domestic", False) == 1500.0


def test_international_flight():
    # TC-05. Обычный багаж на международном рейсе
    # Тип: позитивный. Приоритет: Medium.
    # Вход: weight=20, flight=international, premium=False.
    # Ожидание: (20 - 10) * 250 = 2500.00.
    assert calculate_baggage_fee(20, "international", False) == 2500.0


def test_heavy_baggage_boundary():
    # TC-06. Верхняя граница без сбора за тяжёлый багаж
    # Тип: граничный. Приоритет: High.
    # Вход: weight=30, flight=domestic, premium=False.
    # Ожидание: (30 - 10) * 150 = 3000.00, дополнительного сбора нет.
    assert calculate_baggage_fee(30, "domestic", False) == 3000.0


def test_heavy_baggage_fee():
    # TC-07. Тяжёлый багаж на внутреннем рейсе
    # Тип: граничный. Приоритет: High.
    # Вход: weight=31, flight=domestic, premium=False.
    # Ожидание: (31 - 10) * 150 + 1000 = 4150.00.
    assert calculate_baggage_fee(31, "domestic", False) == 4150.0


def test_heavy_baggage_international():
    # TC-08. Тяжёлый багаж на международном рейсе
    # Тип: позитивный. Приоритет: Medium.
    # Вход: weight=31, flight=international, premium=False.
    # Ожидание: (31 - 10) * 250 + 1000 = 6250.00.
    assert calculate_baggage_fee(31, "international", False) == 6250.0


def test_maximum_weight():
    # TC-09. Максимально допустимый вес
    # Тип: граничный. Приоритет: High.
    # Вход: weight=50, flight=domestic, premium=False.
    # Ожидание: (50 - 10) * 150 + 1000 = 7000.00.
    assert calculate_baggage_fee(50, "domestic", False) == 7000.0


def test_premium_discount():
    # TC-10. Premium-скидка на обычный багаж
    # Тип: позитивный. Приоритет: High.
    # Вход: weight=20, flight=domestic, premium=True.
    # Ожидание: ((20 - 10) * 150) * 0.7 = 1050.00.
    assert calculate_baggage_fee(20, "domestic", True) == 1050.0


def test_premium_with_heavy_baggage():
    # TC-11. Premium-скидка на тяжёлый багаж
    # Тип: позитивный. Приоритет: High.
    # Вход: weight=31, flight=domestic, premium=True.
    # Ожидание: ((31 - 10) * 150 + 1000) * 0.7 = 2905.00.
    assert calculate_baggage_fee(31, "domestic", True) == 2905.0


def test_free_baggage_for_premium():
    # TC-12. Бесплатный багаж для premium-пассажира
    # Тип: позитивный. Приоритет: Medium.
    # Вход: weight=10, flight=international, premium=True.
    # Ожидание: багаж до 10 кг бесплатный, стоимость после скидки остаётся 0.00.
    assert calculate_baggage_fee(10, "international", True) == 0.0


def test_negative_weight():
    # TC-13. Отрицательный вес багажа
    # Тип: негативный. Приоритет: High.
    # Вход: weight=-1, flight=domestic, premium=False.
    # Ожидание: ValueError, так как вес не может быть меньше 0.
    with pytest.raises(ValueError):
        calculate_baggage_fee(-1, "domestic", False)


def test_weight_over_limit():
    # TC-14. Вес выше максимально допустимого
    # Тип: негативный. Приоритет: High.
    # Вход: weight=50.01, flight=domestic, premium=False.
    # Ожидание: ValueError, так как вес больше 50 кг.
    with pytest.raises(ValueError):
        calculate_baggage_fee(50.01, "domestic", False)


def test_invalid_flight_type():
    # TC-15. Некорректный тип рейса
    # Тип: негативный. Приоритет: High.
    # Вход: weight=20, flight=space, premium=False.
    # Ожидание: ValueError, так как допустимы только domestic и international.
    with pytest.raises(ValueError):
        calculate_baggage_fee(20, "space", False)
