import polars as pl

from dqframework.validators import HasStrMaxLength


def test_has_max_length():
    df = pl.DataFrame({"a": ["a", "ab", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrMaxLength("a", 1).execute(df)

    assert correct.height == 1

    assert incorrect.height == 2


def test_has_max_length_with_no_incorrects():
    df = pl.DataFrame({"a": ["acb", "bac", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrMaxLength("a", 3).execute(df)

    assert correct.height == 3
    assert incorrect.height == 0


def test_has_max_length_with_all_incorrects():
    df = pl.DataFrame({"a": ["acb", "bac", "abc"], "b": ["abcd", "abcde", "abcdef"]})

    correct, incorrect = HasStrMaxLength("a", 0).execute(df)

    assert correct.height == 0
    assert incorrect.height == 3
