import polars as pl

from dqframework.validators import HasStrMinLength


def test_has_max_length():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrMinLength("a", 2).execute(df)

    assert correct.height == 2

    assert incorrect.height == 1


def test_has_max_length_with_no_incorrects():
    df = pl.DataFrame({"a": ["acb", "bac", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrMinLength("a", 0).execute(df)

    assert correct.height == 3
    assert incorrect.height == 0


def test_has_max_length_with_all_incorrects():
    df = pl.DataFrame({"a": ["acb", "bac", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrMinLength("a", 10).execute(df)

    assert correct.height == 0
    assert incorrect.height == 3
