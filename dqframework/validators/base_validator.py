import abc
from typing import Optional, Any

import polars as pl

class Validator(abc.ABC):
    def __init__(self, column: str | list[str], value: Optional[Any] = None):
        self.column = column
        self.value = value

    def execute(self, df: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
        return df, df

    def get_value(self):
        return self.value
