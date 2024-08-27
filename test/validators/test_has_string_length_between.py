import polars as pl

from dqframework.validators import has_string_length_between


def test_has_string_length_between():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = has_string_length_between(df, "a", 1, 2)

    assert correct.shape[0] == 2
    assert correct.height == 2

    assert incorrect.shape[0] == 1


def test_has_all_incorrect():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = has_string_length_between(df, "a", 4, 5)

    assert correct.height == 0
    assert incorrect.height == 3


def test_has_all_correct():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = has_string_length_between(df, "a", 1, 3)

    assert correct.height == 3
    assert incorrect.height == 0
