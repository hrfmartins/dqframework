import polars as pl

from dqframework.pipeline import Pipeline, Check
from dqframework.validators import has_date_pattern


def test_has_date_pattern():
    pipeline = Pipeline(checks=[])
    check1 = Check(Check.Level.INFO, "Has Date Pattern")
    check1.validations.append([has_date_pattern, "a", "%Y-%m-%d"])

    pipeline.checks += [check1]

    (valid, invalid, result) = pipeline.execute(
        pl.DataFrame({"a": ["2021-01-01", "2021-02-01", "2021-03-01"], "b": [4, 5, 6]})
    )

    assert valid.height == 3
    assert invalid.height == 0


def test_has_two_invalids():
    pipeline = Pipeline(checks=[])
    check1 = Check(Check.Level.INFO, "Has Date Pattern")
    check1.validations.append([has_date_pattern, "a", "%Y-%m-%d"])

    pipeline.checks += [check1]

    (valid, invalid, result) = pipeline.execute(
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

    assert valid.height == 1
    assert invalid.height == 2
    assert invalid["a"].to_list() == ["02-2022-01", "2021-13-13"]
