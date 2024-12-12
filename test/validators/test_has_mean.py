import polars as pl

from dqframework.validators.comparisons_operator import ComparisonsOperator
from dqframework.validators.has_mean import HasMean


def test_has_mean():
    df = pl.DataFrame({"a": [1, 1, 1, 1, 1]})

    results = HasMean("a", 3, ComparisonsOperator.LESS).execute(df)

    assert results[0].height == 5


def test_has_wrong_mean():
    df = pl.DataFrame({"a": [1, 1, 1, 1, 1]})

    results = HasMean("a", 3, ComparisonsOperator.GREATER).execute(df)

    assert results[0].height == 0
    assert results[1].height == 5


def test_has_mean_bigger_than():
    df = pl.DataFrame({"a": [1, 2, 3, 4, 5]})

    results = HasMean("a", 3, ComparisonsOperator.GREATER).execute(df)

    assert results[0].height == 0
    assert results[1].height == 5


def test_has_bigger_than_or_equal():
    df = pl.DataFrame({"a": [1, 2, 3, 4, 5]})

    results = HasMean("a", 3, ComparisonsOperator.GREATER_EQUAL).execute(df)

    assert results[0].height == 5
    assert results[1].height == 0


def test_has_mean_smaller_than():
    df = pl.DataFrame({"a": [1, 2, 3, 4, 5]})

    results = HasMean("a", 3, ComparisonsOperator.LESS).execute(df)

    assert results[0].height == 0
    assert results[1].height == 5


def test_has_smaller_than_or_equal():
    df = pl.DataFrame({"a": [1, 2, 3, 4, 5]})

    results = HasMean("a", 3, ComparisonsOperator.LESS_EQUAL).execute(df)

    assert results[0].height == 5
    assert results[1].height == 0


def test_has_mean_with_value_out_of_comparison_operator():
    df = pl.DataFrame({"a": [1, 2, 3, 4, 5]})

    try:
        HasMean("a", 3, "GREATER_EQUAL").execute(df)
    except ValueError as e:
        assert str(e) == "comparison_op must be a ComparisonsOperator"
    else:
        assert False
