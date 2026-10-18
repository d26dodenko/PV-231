import pytest
from salary import calculate_salary


def test_regular_salary():
    assert calculate_salary(160000, 160, 1.5, False) == pytest.approx(160000)


def test_penalty_below_80_hours():
    assert calculate_salary(160000, 79, 1.5, False) == pytest.approx(128000)


def test_no_penalty_at_80_hours():
    assert calculate_salary(160000, 80, 1.5, False) == pytest.approx(160000)


def test_no_bonus_below_160_hours():
    assert calculate_salary(160000, 159, 1.5, True) == pytest.approx(160000)


def test_bonus_at_160_hours():
    assert calculate_salary(160000, 160, 1.5, True) == pytest.approx(192000)


def test_overtime_without_bonus():
    assert calculate_salary(160000, 170, 1.5, False) == pytest.approx(175000)


def test_overtime_with_bonus():
    assert calculate_salary(160000, 170, 1.5, True) == pytest.approx(210000)


def test_zero_base_salary():
    assert calculate_salary(0, 170, 1.5, True) == pytest.approx(0)


def test_zero_worked_hours():
    assert calculate_salary(160000, 0, 1.5, False) == pytest.approx(128000)


def test_negative_base_salary():
    with pytest.raises(ValueError):
        calculate_salary(-1, 160, 1.5, False)


def test_negative_worked_hours():
    with pytest.raises(ValueError):
        calculate_salary(160000, -1, 1.5, False)


def test_negative_overtime_rate():
    with pytest.raises(ValueError):
        calculate_salary(160000, 170, -1, False)