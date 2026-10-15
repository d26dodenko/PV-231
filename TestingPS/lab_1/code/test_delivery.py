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