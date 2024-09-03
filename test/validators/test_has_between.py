import polars as pl

from dqframework.validators import HasBetween


def test_has_between():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = HasBetween("a", 1, 2).validate(df)

    assert correct.shape[0] == 2
    assert correct.height == 2

    assert incorrect.shape[0] == 1


def test_has_all_incorrect():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = HasBetween("a", 4, 5).validate(df)

    assert correct.height == 0
    assert incorrect.height == 3


def test_has_all_correct():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    correct, incorrect = HasBetween("a", 1, 3).validate(df)

    assert correct.height == 3
    assert incorrect.height == 0
