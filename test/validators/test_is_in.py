import polars as pl

from dqframework.validators import is_in


def test_is_in():
    df = pl.DataFrame({"a": ["AA", "AAA", "BB"], "b": [4, 5, 6]})

    correct, incorrect = is_in(df, "a", ["AAA", "AA", "BB"])

    assert correct.height == 3
    assert incorrect.height == 0


def test_is_in_with_some_corrects():
    df = pl.DataFrame({"a": ["AA", "AAA", "BB"], "b": [4, 5, 6]})

    correct, incorrect = is_in(df, "a", ["AA", "BB"])

    assert correct.height == 2
    assert incorrect.height == 1


def test_is_in_with_no_corrects():
    df = pl.DataFrame({"a": ["AA", "AAA", "BB"], "b": [4, 5, 6]})

    correct, incorrect = is_in(df, "a", ["CC"])

    assert correct.height == 0
    assert incorrect.height == 3
