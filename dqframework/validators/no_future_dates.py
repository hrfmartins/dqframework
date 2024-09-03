import datetime

import polars as pl

from .base_validator import Validator


class NoFutureDates(Validator):
    """
    Check if a DataFrame column contains no future dates

    Parameters
    :param column: name of the column to check
    :param date: datetime.datetime (default is right now)
    """

    def __init__(self, column: str, date: datetime = datetime.datetime.now()):
        super().__init__(column, date)

    def execute(self, df: pl.DataFrame):
        correct = df.filter(pl.col(self.column) <= pl.lit(self.value))
        incorrect = df.filter(pl.col(self.column) > pl.lit(self.value))

        return correct, incorrect
