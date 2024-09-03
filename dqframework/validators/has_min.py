import polars as pl

from .base_validator import Validator


class HasMin(Validator):
    """
    Check if a DataFrame column has a minimum value of value

    Parameters
    :param column: name of the column to check
    :param value: minimum value to check
    """

    def __init__(self, column: str, value: int):
        super().__init__(column, value)

    def execute(self, df: pl.DataFrame):
        correct = df.filter(pl.col(self.column) >= self.value)
        incorrect = df.filter(pl.col(self.column) < self.value)

        return correct, incorrect
