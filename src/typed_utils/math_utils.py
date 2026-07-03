"""Typed arithmetic and numeric helper functions."""

from __future__ import annotations

Number = int | float


def add(a: Number, b: Number) -> Number:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Return a minus b."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Return the product of two numbers."""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Divide a by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def average(numbers: list[Number]) -> float:
    """Return the arithmetic mean of a list of numbers.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot compute the average of an empty list.")
    return sum(numbers) / len(numbers)


def clamp(value: Number, low: Number, high: Number) -> Number:
    """Clamp value to the inclusive range [low, high].

    Raises:
        ValueError: If low is greater than high.
    """
    if low > high:
        raise ValueError("low cannot be greater than high.")
    return max(low, min(value, high))
