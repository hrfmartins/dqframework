import polars as pl

from dqframework.pipeline import Pipeline, Check
from dqframework.validators import HasDatePattern


def test_has_date_pattern():
    pipeline = Pipeline(checks=[])
    check1 = Check(Check.Level.INFO, "Has Date Pattern")
    check1.validations.append(HasDatePattern("a", "%Y-%m-%d"))

    pipeline.checks += [check1]

    pipeline_results = pipeline.execute(
        pl.DataFrame({"a": ["2021-01-01", "2021-02-01", "2021-03-01"], "b": [4, 5, 6]})
    )

    assert pipeline_results.valid_records.height == 3
    assert pipeline_results.invalid_records.height == 0


def test_has_two_invalids():
    pipeline = Pipeline(checks=[])
    check1 = Check(Check.Level.ERROR, "Has Date Pattern")
    check1.validations.append(HasDatePattern("a", "%Y-%m-%d"))

    pipeline.checks += [check1]

    pipeline_results = pipeline.execute(
        pl.DataFrame(
            {
                "a": [
                    "2021-01-01",
                    "02-2022-01",
                    "2021-13-13",
                ],
                "b": [4, 5, 6],
            }
        )
    )

    assert pipeline_results.valid_records.height == 1
    assert pipeline_results.invalid_records.height == 2
    assert pipeline_results.invalid_records["a"].to_list() == [
        "02-2022-01",
        "2021-13-13",
    ]
