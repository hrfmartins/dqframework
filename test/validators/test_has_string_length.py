import polars as pl

from dqframework.validators import has_string_length


def test_has_string_length():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = has_string_length(df, "a", 1)

    assert correct.shape[0] == 1
    assert correct.height == 1

    assert incorrect.shape[0] == 2


def test_has_string_length_with_no_incorrects():
    df = pl.DataFrame({"a": ["acb", "bac", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = has_string_length(df, "a", 3)

    assert correct.height == 3
    assert incorrect.height == 0
