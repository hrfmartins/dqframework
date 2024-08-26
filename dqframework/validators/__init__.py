import abc

import polars as pl


class Validator(abc.ABC):
    def __init__(self):
        pass

    def validate(self, df: pl.DataFrame) -> (pl.DataFrame, pl.DataFrame):
        pass
