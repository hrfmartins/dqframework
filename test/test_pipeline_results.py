from datetime import timedelta

import polars as pl

from dqframework.pipeline import Pipeline, Check
from dqframework.validators.has_min import has_min


def test_pipeline_results():
    pipeline = Pipeline(checks=[])
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 2])

    pipeline.checks += [check1]

    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )

    assert results.height == len(pipeline.checks)
    assert results["pass_rate"][0] == 2 / 3
    assert results["status"][0] == "FAIL"
    assert results["violations"][0] == 1
    assert results["level"][0] == "INFO"


def test_pipeline_results_with_warning_error():
    check1 = Check(Check.Level.WARNING, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 2])

    pipeline = Pipeline([check1])

    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )

    assert results.height == len(pipeline.checks)
    assert results["pass_rate"][0] == 2 / 3
    assert results["status"][0] == "FAIL"
    assert results["violations"][0] == 1
    assert results["level"][0] == "WARNING"


def test_pipeline_results_attributes():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 2])

    pipeline = Pipeline([check1])

    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )

    assert results["check_id"][0] != ""
    assert results["id"][0] != ""
    # timestamp is within a 10 sec range
    assert results["timestamp"][0] - timedelta(seconds=1)

    assert results["check"][0] == "Has Minimum Value 2"
    assert results["column"][0] == "a"
    assert results["rule"][0] == "has_min"
    assert results["value"][0] == "2"
    assert results["rows"][0] == 3
    assert results["violations"][0] == 1
    assert results["pass_rate"][0] == 2 / 3
    assert results["pass_threshold"][0] == 0.9


def test_pipeline_with_custom_threshold():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 0", pass_threshold=0.5)
    check1.validations.append([has_min, "a", 0])

    pipeline = Pipeline([check1])

    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )

    assert results["status"][0] == "PASS"


def test_pipeline_with_custom_threshold_and_fails():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2", pass_threshold=0.9)
    check1.validations.append([has_min, "a", 2])

    pipeline = Pipeline([check1])

    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )

    assert results["status"][0] == "FAIL"


def test_pipeline_check_with_multiple_validations():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2 and 4")
    check1.validations.append([has_min, "a", 2])
    check1.validations.append([has_min, "b", 4])

    pipeline = Pipeline([check1])

    (valid, invalid, results) = pipeline.execute(
        pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    )

    assert results.height == 2
    assert results["status"][0] == "FAIL"
    assert results["violations"][0] == 1
    assert results["pass_rate"][0] == 2 / 3
    assert results["level"][0] == "INFO"
    assert results["column"][0] == "a"

    assert results["status"][1] == "PASS"
    assert results["violations"][1] == 0
    assert results["pass_rate"][1] == 1
    assert results["level"][1] == "INFO"
    assert results["column"][1] == "b"
