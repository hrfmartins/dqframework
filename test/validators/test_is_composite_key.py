import polars as pl

from dqframework.validators import is_composite_key


def test_is_composite_key():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = is_composite_key(df, ["a", "b"])

    assert correct.shape[0] == 3
    assert correct.height == 3

    assert incorrect.shape[0] == 0


def test_is_composite_key_with_some_corrects():
    df = pl.DataFrame({"a": [1, 2, 2], "b": [4, 5, 5]})

    correct, incorrect = is_composite_key(df, ["a", "b"])

    assert correct.height == 1
    assert incorrect.height == 2
