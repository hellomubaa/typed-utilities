"""Typed list helper functions."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def flatten(nested: list[list[T]]) -> list[T]:
    """Flatten a list of lists into a single list."""
    return [item for sublist in nested for item in sublist]


def unique(items: list[T]) -> list[T]:
    """Return items with duplicates removed, preserving order."""
    seen: set[T] = set()
    result: list[T] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def chunk(items: list[T], size: int) -> list[list[T]]:
    """Split items into chunks of at most `size` elements.

    Raises:
        ValueError: If size is not a positive integer.
    """
    if size <= 0:
        raise ValueError("size must be a positive integer.")
    return [items[i : i + size] for i in range(0, len(items), size)]


def find_first(items: list[T], predicate: Callable[[T], bool]) -> T | None:
    """Return the first item matching predicate, or None if not found."""
    for item in items:
        if predicate(item):
            return item
    return None
