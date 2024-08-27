import datetime

import polars as pl

from dqframework.validators import no_future_dates


def test_no_future_dates():
    df = pl.DataFrame(
        {
            "a": [
                datetime.datetime.strptime("2022-01-01", "%Y-%m-%d"),
                datetime.datetime.strptime("2023-01-01", "%Y-%m-%d"),
                datetime.datetime.strptime("2024-01-01", "%Y-%m-%d"),
            ],
            "b": [4, 5, 6],
        }
    )

    correct, incorrect = no_future_dates(df, "a")

    assert correct.shape[0] == 3
    assert correct.height == 3

    assert incorrect.shape[0] == 0


def test_no_future_dates_with_some_corrects():
    df = pl.DataFrame(
        {
            "a": [
                datetime.datetime.strptime("2022-01-01", "%Y-%m-%d"),
                datetime.datetime.strptime("2024-12-01", "%Y-%m-%d"),
                datetime.datetime.strptime("2021-01-01", "%Y-%m-%d"),
            ],
            "b": [4, 5, 6],
        }
    )

    correct, incorrect = no_future_dates(df, "a")

    assert correct.height == 2
    assert incorrect.height == 1


def test_no_future_dates_with_all_incorrect():
    df = pl.DataFrame(
        {
            "a": [
                datetime.datetime.strptime("2025-01-01", "%Y-%m-%d"),
                datetime.datetime.strptime("2025-01-01", "%Y-%m-%d"),
                datetime.datetime.strptime("2025-01-01", "%Y-%m-%d"),
            ],
            "b": [4, 5, 6],
        }
    )

    correct, incorrect = no_future_dates(df, "a")

    assert correct.height == 0
    assert incorrect.height == 3
