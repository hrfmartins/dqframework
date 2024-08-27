import polars as pl

from dqframework.pipeline import Check, Pipeline
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


def test_is_unique_in_a_pipeline():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    check = Check(Check.Level.INFO, "Is Unique")

    check.validations.append([is_unique, "a"])

    pipeline = Pipeline(checks=[check])
    pipeline_results = pipeline.execute(df)

    assert pipeline_results.valid_records.height == 3
