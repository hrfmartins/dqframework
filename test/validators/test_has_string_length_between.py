import polars as pl

from dqframework.validators import HasStrLengthBetween


def test_has_string_length_between():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrLengthBetween("a", 1, 2).execute(df)

    assert correct.shape[0] == 2
    assert correct.height == 2

    assert incorrect.shape[0] == 1


def test_has_all_incorrect():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrLengthBetween("a", 4, 5).execute(df)

    assert correct.height == 0
    assert incorrect.height == 3


def test_has_all_correct():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrLengthBetween("a", 1, 3).execute(df)

    assert correct.height == 3
    assert incorrect.height == 0
