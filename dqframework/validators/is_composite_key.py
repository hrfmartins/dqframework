import polars as pl

from .base_validator import Validator


class IsCompositeKey(Validator):
    """
    Check if a list of DataFrame columns form a composite key (unique values)

    Parameters
    :param columns: list of columns to check
    """

    def __init__(self, columns: list[str]):
        super().__init__(columns)
        self.columns = columns

    def execute(self, df: pl.DataFrame):
        correct = df.filter(df.select(self.columns).is_unique())
        incorrect = df.filter(~df.select(self.columns).is_unique())

        return correct, incorrect
