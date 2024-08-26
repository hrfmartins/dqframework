import polars as pl

from dqframework.validators.has_min import has_min


def test_is_min():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = has_min(df, "a", 2)

    assert correct.shape[0] == 2
    assert correct.height == 2

    assert incorrect.shape[0] == 1


def test_is_min_with_no_filter():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = has_min(df, "a", 0)

    assert correct.height == 3
    assert incorrect.height == 0
