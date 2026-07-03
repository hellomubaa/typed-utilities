import pytest

from typed_utils.math_utils import add, average, clamp, divide, multiply, subtract


def test_add_normal():
    assert add(2, 3) == 5


def test_add_floats():
    assert add(2.5, 0.5) == 3.0


def test_subtract_normal():
    assert subtract(10, 4) == 6


def test_multiply_normal():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(5, 0) == 0


def test_divide_normal():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(5, 0)


def test_average_normal():
    assert average([2, 4, 6]) == 4


def test_average_empty_raises():
    with pytest.raises(ValueError):
        average([])


def test_clamp_within_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_low():
    assert clamp(-5, 0, 10) == 0


def test_clamp_above_high():
    assert clamp(15, 0, 10) == 10


def test_clamp_invalid_range_raises():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)
