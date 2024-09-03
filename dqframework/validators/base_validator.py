import abc
from typing import Optional

import polars as pl


class Validator(abc.ABC):
    def __init__(self, column: str | list[str], value: Optional = None):
        self.column = column
        self.value = value

    def execute(self, df: pl.DataFrame):
        pass

    def get_value(self):
        return self.value
