"""typed_utils: a small typed utility package for math, string, and list helpers."""

from .list_utils import chunk, find_first, flatten, unique
from .math_utils import add, average, clamp, divide, multiply, subtract
from .string_utils import is_palindrome, reverse, to_snake_case, truncate, word_count

__all__ = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "average",
    "clamp",
    "reverse",
    "is_palindrome",
    "word_count",
    "truncate",
    "to_snake_case",
    "flatten",
    "unique",
    "chunk",
    "find_first",
]

__version__ = "0.1.0"
