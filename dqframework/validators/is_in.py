import polars as pl

from .base_validator import Validator


class IsIn(Validator):
    """
    Check if a DataFrame column has values in a list

    Parameters
    :param column: name of the column to check
    :param values: list of values to check
    """

    def __init__(self, column: str, values: list):
        super().__init__(column, values)
        self.values = values

    def execute(self, df: pl.DataFrame):
        correct = df.filter(pl.col(self.column).is_in(self.values))
        incorrect = df.filter(~pl.col(self.column).is_in(self.values))

        return correct, incorrect
