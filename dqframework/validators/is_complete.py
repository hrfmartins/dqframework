import polars as pl

from .base_validator import Validator


class IsComplete(Validator):
    """
    Check if a DataFrame column is complete

    Parameters
    :param column: name of the column to check
    """

    def __init__(self, column: str):
        super().__init__(column)

    def execute(self, df: pl.DataFrame):
        correct = df.filter(pl.col(self.column).is_not_null())
        incorrect = df.filter(pl.col(self.column).is_null())

        return correct, incorrect
