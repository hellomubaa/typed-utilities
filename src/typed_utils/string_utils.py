"""Typed string helper functions."""

from __future__ import annotations


def reverse(text: str) -> str:
    """Return the reversed string."""
    return text[::-1]


def is_palindrome(text: str) -> bool:
    """Return True if text reads the same forwards and backwards.

    Comparison ignores case and non-alphanumeric characters.
    """
    cleaned = [ch.lower() for ch in text if ch.isalnum()]
    return cleaned == cleaned[::-1]


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in text."""
    return len(text.split())


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length characters, appending suffix if cut.

    Raises:
        ValueError: If max_length is negative.
    """
    if max_length < 0:
        raise ValueError("max_length cannot be negative.")
    if len(text) <= max_length:
        return text
    if max_length <= len(suffix):
        return suffix[:max_length]
    return text[: max_length - len(suffix)] + suffix


def to_snake_case(text: str) -> str:
    """Convert a space- or camelCase-separated string to snake_case."""
    result: list[str] = []
    for i, ch in enumerate(text):
        if ch.isupper() and i != 0:
            result.append("_")
        if ch.isspace():
            result.append("_")
        elif not ch.isspace():
            result.append(ch.lower())
    snake = "".join(result)
    while "__" in snake:
        snake = snake.replace("__", "_")
    return snake.strip("_")
