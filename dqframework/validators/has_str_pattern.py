import polars as pl

from .base_validator import Validator


class HasStrPattern(Validator):
    """
    Check if a DataFrame column has a string pattern

    Parameters
    :param column: name of the column to check
    :param value: pattern to check
    """

    def __init__(self, column: str, value: str):
        super().__init__(column, value)

    def execute(self, df: pl.DataFrame):
        correct = df.filter(pl.col(self.column).str.contains(self.value))
        incorrect = df.filter(~pl.col(self.column).str.contains(self.value))

        return correct, incorrect
