import pytest
from calculator import (
    add, subtract, multiply,
    divide, classify_number
)


def test_add():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-2, -3) == -5


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(3, 4) == 12


def test_multiply_zero():
    assert multiply(5, 0) == 0


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)


def test_positive():
    assert classify_number(5) == "positive"


def test_zero():
    assert classify_number(0) == "zero"


def test_negative():
    assert classify_number(-5) == "negative"
