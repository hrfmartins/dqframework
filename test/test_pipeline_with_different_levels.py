import polars as pl
import pytest

from dqframework.pipeline import Check, Pipeline
from dqframework.validators.has_max import HasMax


@pytest.fixture
def test_dataframe():
    return pl.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David"],
            "age": [24, 25, 26, 27],
        }
    )


def test_pipeline_with_info_level(test_dataframe):
    check = Check(Check.Level.INFO, "Check With Info Level")
    check.validations = [HasMax("age", 25)]

    pipeline = Pipeline(checks=[check])

    results = pipeline.execute(test_dataframe)

    assert results.results.to_dicts()[0]["level"] == Check.Level.INFO.value
    assert results.valid_records.to_dicts() == test_dataframe.to_dicts()
    assert results.valid_records.height == 4


def test_pipeline_with_warning_level(test_dataframe):
    check = Check(Check.Level.WARNING, "Check With Warning Level")
    check.validations = [HasMax("age", 25)]

    pipeline = Pipeline(checks=[check])

    results = pipeline.execute(test_dataframe)

    assert results.results.to_dicts()[0]["level"] == Check.Level.WARNING.value
    assert results.valid_records.to_dicts() == test_dataframe.to_dicts()
    assert results.valid_records.height == 4


def test_pipeline_with_error_level(test_dataframe):
    check = Check(Check.Level.ERROR, "Check With Error Level")
    check.validations = [HasMax("age", 25)]

    pipeline = Pipeline(checks=[check])

    results = pipeline.execute(test_dataframe)

    assert results.results.to_dicts()[0]["level"] == Check.Level.ERROR.value
    assert results.valid_records.height == 2


def test_pipeline_with_critical_level(test_dataframe):
    check = Check(Check.Level.CRITICAL, "Check With Critical Level")
    check.validations = [HasMax("age", 25)]

    pipeline = Pipeline(checks=[check])

    results = pipeline.execute(test_dataframe)

    assert results.results.to_dicts()[0]["level"] == Check.Level.CRITICAL.value
    assert results.valid_records.height == 2
    assert results.results.to_dicts()[0]["status"] == "FAIL"
    assert results.results.to_dicts()[0]["violations"] == 2
    assert results.results.to_dicts()[0]["pass_rate"] == 1 / 2
