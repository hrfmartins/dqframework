import polars as pl

from dqframework.pipeline import Pipeline, Check
from dqframework.validators.has_min import has_min


def test_pipeline_with_checks():
    pipeline = Pipeline(checks=[])
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 2])

    pipeline.checks += [check1]

    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )

    assert valid.height == 2


def test_pipeline_with_multiple_checks():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 2])
    check2 = Check(Check.Level.INFO, "Has Minimum Value 1")
    check2.validations.append([has_min, "a", 1])

    pipeline = Pipeline(checks=[check1, check2])
    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )

    assert valid.height == 2
    assert invalid.height == 1


def test_pipeline_with_no_checks():
    pipeline = Pipeline(checks=[])
    try:
        pipeline.execute(pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    except ValueError as e:
        assert str(e) == "No checks added to the pipeline"


def test_check_with_no_validations():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    pipeline = Pipeline(checks=[check1])
    try:
        pipeline.execute(pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    except ValueError as e:
        assert str(e) == "No validations added to the check"


def test_pipeline_with_no_filtered_records():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 0])
    pipeline = Pipeline(checks=[check1])
    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )
    assert valid.height == 3
    assert invalid.height == 0


def test_pipeline_with_all_incorrect_records():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 4])
    pipeline = Pipeline(checks=[check1])
    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )
    assert valid.height == 0
    assert invalid.height == 3
