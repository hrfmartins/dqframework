import polars as pl

from .base_validator import Validator


class HasBetween(Validator):
    def __init__(self, column: str, min_value: int, max_value: int):
        super().__init__(column, (min_value, max_value))
        self.min_value = min_value
        self.max_value = max_value

    def execute(self, df: pl.DataFrame) -> (pl.DataFrame, pl.DataFrame):
        correct = df.filter(
            (pl.col(self.column) >= self.min_value)
            & (pl.col(self.column) <= self.max_value)
        )
        incorrect = df.filter(
            (pl.col(self.column) < self.min_value)
            | (pl.col(self.column) > self.max_value)
        )

        return correct, incorrect
