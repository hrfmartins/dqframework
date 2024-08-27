import polars as pl

from dqframework.validators import is_unique


def test_is_unique():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = is_unique(df, "a")

    assert correct.shape[0] == 3
    assert correct.height == 3

    assert incorrect.shape[0] == 0


def test_is_unique_with_some_corrects():
    df = pl.DataFrame({"a": [1, 2, 2], "b": [4, 5, 6]})

    correct, incorrect = is_unique(df, "a")

    assert correct.height == 1
    assert incorrect.height == 2


def test_is_unique_with_no_corrects():
    df = pl.DataFrame({"a": [1, 1, 1], "b": [4, 5, 6]})

    correct, incorrect = is_unique(df, "a")

    assert correct.height == 0
    assert incorrect.height == 3
