import polars as pl

from dqframework.validators.base_validator import Validator


class HasDatePattern(Validator):
    """
    Check if a DataFrame column has a date pattern

    Parameters
    :param column: name of the column to check
    :param pattern: pattern to check
    """

    def __init__(self, column: str, pattern: str):
        super().__init__(column, pattern)
        self.pattern = pattern

    def execute(self, df: pl.DataFrame):
        correct = df.filter(
            pl.col(self.column).str.to_date(self.pattern, strict=False).is_not_null()
        )
        incorrect = df.filter(
            pl.col(self.column).str.to_date(self.pattern, strict=False).is_null()
        )

        return correct, incorrect
