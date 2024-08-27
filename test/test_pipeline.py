import polars as pl

from dqframework.pipeline import Pipeline, Check
from dqframework.validators import has_min, is_complete, has_string_pattern


def test_pipeline_with_checks():
    pipeline = Pipeline(checks=[])
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 2])

    pipeline.checks += [check1]

    pipeline_results = pipeline.execute(pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))

    assert pipeline_results.valid_records.height == 2


def test_pipeline_with_multiple_checks():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 2])
    check2 = Check(Check.Level.INFO, "Has Minimum Value 1")
    check2.validations.append([has_min, "a", 1])

    pipeline = Pipeline(checks=[check1, check2])
    pipeline_results = pipeline.execute(pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))

    assert pipeline_results.valid_records.height == 2
    assert pipeline_results.invalid_records.height == 1


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
    pipeline_results = pipeline.execute(pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    assert pipeline_results.valid_records.height == 3
    assert pipeline_results.invalid_records.height == 0


def test_pipeline_with_all_incorrect_records():
    check1 = Check(Check.Level.INFO, "Has Minimum Value 2")
    check1.validations.append([has_min, "a", 4])
    pipeline = Pipeline(checks=[check1])
    pipeline_results = pipeline.execute(pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    assert pipeline_results.valid_records.height == 0
    assert pipeline_results.invalid_records.height == 3


def test_pipeline_with_multiple_checks_with_multiple_validations():
    check1 = Check(Check.Level.INFO, "Minimum of cards and age is 1")
    check1.validations.append([is_complete, "Cards_Collected"])
    check1.validations.append([has_min, "Cards_Collected", 1])
    check1.validations.append([has_min, "Age", 1])

    check2 = Check(Check.Level.INFO, "All names are valid")
    check2.validations.append([is_complete, "Name"])
    check2.validations.append([has_string_pattern, "Name", "\w{3,20}"])

    pipeline = Pipeline([check1, check2])

    pipeline_results = pipeline.execute(
        pl.DataFrame(
            {
                "Name": ["John", "A", "Bob"],
                "Age": [21, 35, 27],
                "Cards_Collected": [0, 5, 6],
            }
        )
    )

    results = pipeline_results.results

    assert results.height == len(check1.validations) + len(check2.validations)
    assert pipeline_results.invalid_records.height == 2
    assert results["status"][0] == "PASS"
    assert results["status"][1] == "FAIL"  # Cards collected has a 0
    assert results["status"][2] == "PASS"
    assert results["status"][3] == "PASS"
    assert results["status"][4] == "FAIL"  # Name A is not valid


def test_pipeline_div_by_zero():
    # If records run out before pipeline ends, we should not divide by zero and so it should be 0 on the pass rate
    check1 = Check(Check.Level.INFO, "Has Minimum Value 1")
    check1.validations.append([has_min, "a", 10])

    check2 = Check(Check.Level.INFO, "Has Minimum Value 1")
    check2.validations.append([has_min, "a", 0])

    pipeline = Pipeline(checks=[check1, check2])
    pipeline_results = pipeline.execute(pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))

    assert pipeline_results.invalid_records.height == 3
    assert pipeline_results.results["pass_rate"].to_list() == [0.0, 0.0]
