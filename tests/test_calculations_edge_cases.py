import pytest

from src.calculations import area_of_circle, get_nth_fibonacci


def test_area_of_circle_rejects_negative_radius():
    with pytest.raises(ValueError, match="Radius cannot be negative"):
        area_of_circle(-1)


def test_get_nth_fibonacci_calculates_larger_value():
    assert get_nth_fibonacci(10) == 55


def test_get_nth_fibonacci_rejects_negative_index():
    with pytest.raises(ValueError, match="n cannot be negative"):
        get_nth_fibonacci(-1)
