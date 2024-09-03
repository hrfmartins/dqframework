import polars as pl

from .base_validator import Validator


class IsUnique(Validator):
    """
    Check if a DataFrame column contains only unique values

    Parameters
    :param column: name of the column to check
    """

    def __init__(self, column: str):
        super().__init__(column)

    def execute(self, df: pl.DataFrame):
        correct = df.filter(pl.col(self.column).is_unique())
        incorrect = df.filter(~pl.col(self.column).is_unique())

        return correct, incorrect
