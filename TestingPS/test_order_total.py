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
