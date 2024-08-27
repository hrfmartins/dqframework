import polars as pl

from dqframework.validators import has_max


def test_has_max():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = has_max(df, "a", 2)

    assert correct.shape[0] == 2
    assert correct.height == 2

    assert incorrect.shape[0] == 1


def test_has_max_with_no_corrects():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = has_max(df, "a", 0)

    assert correct.height == 0
    assert incorrect.height == 3


def test_has_max_with_all_corrects():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = has_max(df, "a", 4)

    assert correct.height == 3
    assert incorrect.height == 0
