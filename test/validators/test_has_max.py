import polars as pl

from dqframework.validators import HasMax


def test_has_max():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = HasMax("a", 2).execute(df)

    assert correct.shape[0] == 2
    assert correct.height == 2

    assert incorrect.shape[0] == 1


def test_has_max_with_no_corrects():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = HasMax("a", 0).execute(df)

    assert correct.height == 0
    assert incorrect.height == 3


def test_has_max_with_all_corrects():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = HasMax("a", 4).execute(df)

    assert correct.height == 3
    assert incorrect.height == 0
