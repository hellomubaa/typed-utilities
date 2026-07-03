import pytest

from typed_utils.string_utils import (
    is_palindrome,
    reverse,
    to_snake_case,
    truncate,
    word_count,
)


def test_reverse_normal():
    assert reverse("hello") == "olleh"


def test_reverse_empty_string():
    assert reverse("") == ""


def test_is_palindrome_true():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_is_palindrome_false():
    assert is_palindrome("hello") is False


def test_word_count_normal():
    assert word_count("the quick brown fox") == 4


def test_word_count_empty_string():
    assert word_count("") == 0


def test_truncate_no_cut_needed():
    assert truncate("short", 10) == "short"


def test_truncate_cuts_and_appends_suffix():
    assert truncate("hello world", 8) == "hello..."


def test_truncate_max_length_shorter_than_suffix():
    # When max_length <= len(suffix), only the (clipped) suffix is returned.
    assert truncate("hello world", 2) == ".."
    assert truncate("hello world", 3) == "..."


def test_truncate_negative_length_raises():
    with pytest.raises(ValueError):
        truncate("hello", -1)


def test_to_snake_case_from_camel():
    assert to_snake_case("helloWorldExample") == "hello_world_example"


def test_to_snake_case_from_spaces():
    assert to_snake_case("Hello World") == "hello_world"
