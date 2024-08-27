import polars as pl

from dqframework.validators import is_complete


def test_is_complete():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = is_complete(df, "a")

    assert correct.shape[0] == 3
    assert correct.height == 3

    assert incorrect.shape[0] == 0


def test_is_complete_with_some_corrects():
    df = pl.DataFrame({"a": [1, 2, None], "b": [4, 5, 6]})

    correct, incorrect = is_complete(df, "a")

    assert correct.height == 2
    assert incorrect.height == 1


def test_is_complete_with_no_corrects():
    df = pl.DataFrame({"a": [None, None, None], "b": [4, 5, 6]})

    correct, incorrect = is_complete(df, "a")

    assert correct.height == 0
    assert incorrect.height == 3
