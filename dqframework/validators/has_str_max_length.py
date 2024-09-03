import polars as pl

from .base_validator import Validator


class HasStrMaxLength(Validator):
    """
    Check if a DataFrame column has a maximum string length of value

    Parameters
    :param column: name of the column to check
    :param value: maximum length to check
    """

    def __init__(self, column: str, value: int):
        super().__init__(column, value)
        self.column = column
        self.value = value

    def execute(self, df: pl.DataFrame):
        correct = df.filter(pl.col(self.column).str.len_chars() <= self.value)
        incorrect = df.filter(pl.col(self.column).str.len_chars() > self.value)

        return correct, incorrect
