import pytest

from typed_utils.list_utils import chunk, find_first, flatten, unique


def test_flatten_normal():
    assert flatten([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]


def test_flatten_empty_list():
    assert flatten([]) == []


def test_unique_removes_duplicates_preserves_order():
    assert unique([1, 2, 2, 3, 1, 4]) == [1, 2, 3, 4]


def test_unique_empty_list():
    assert unique([]) == []


def test_chunk_normal():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_invalid_size_raises():
    with pytest.raises(ValueError):
        chunk([1, 2, 3], 0)


def test_find_first_match():
    assert find_first([1, 2, 3, 4], lambda x: x % 2 == 0) == 2


def test_find_first_no_match_returns_none():
    assert find_first([1, 3, 5], lambda x: x % 2 == 0) is None
