import polars as pl

from .base_validator import Validator


class HasStrLengthBetween(Validator):
    """
    Check if a DataFrame column has a string length between min_value and max_value

    Parameters
    :param column: name of the column to check
    :param min_value: minimum length to check
    :param max_value: maximum length to check
    """

    def __init__(self, column: str, min_value: int, max_value: int):
        super().__init__(column, (min_value, max_value))
        self.min_value = min_value
        self.max_value = max_value

    def execute(self, df: pl.DataFrame):
        correct = df.filter(
            (pl.col(self.column).str.len_chars() >= self.min_value)
            & (pl.col(self.column).str.len_chars() <= self.max_value)
        )
        incorrect = df.filter(
            (pl.col(self.column).str.len_chars() < self.min_value)
            | (pl.col(self.column).str.len_chars() > self.max_value)
        )

        return correct, incorrect
