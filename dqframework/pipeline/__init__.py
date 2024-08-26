import enum
from typing import List

import polars as pl

columns = {
    "id": int,
    "timestamp": str,
    "check": str,
    "level": str,
    "column": str,
    "rule": str,
    "value": float,
    "rows": int,
    "violations": int,
    "pass_rate": float,
    "pass_threshold": float,
    "status": str,
}


class Check:
    class Level(enum.Enum):
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"

    def __init__(self, level: Level, check_name: str):
        self.level = level
        self.check_name: str = check_name
        self.validations = []

    def __call__(
        self, df: pl.DataFrame, *args, **kwargs
    ) -> (pl.DataFrame, pl.DataFrame, pl.DataFrame):
        if not self.validations:
            raise ValueError("No validations added to the check")
        correct_acc = pl.DataFrame()
        incorrect_acc = pl.DataFrame()

        for validation in self.validations:
            correct, incorrect = validation[0](df, *validation[1:])
            correct_acc = pl.concat([correct_acc, correct], how="vertical")
            incorrect_acc = pl.concat([incorrect_acc, incorrect], how="vertical")

        return (
            pl.DataFrame(schema=columns),
            correct_acc,
            incorrect_acc,
        )


class Pipeline:
    def __init__(self, checks: List[Check]):
        self.checks = checks

    def execute(self, df: pl.DataFrame):
        if not self.checks:
            raise ValueError("No checks added to the pipeline")

        aux_df = df
        invalid_records = pl.DataFrame()
        for check in self.checks:
            (results, ok, notok) = check(aux_df)

            invalid_records = pl.concat([invalid_records, notok], how="vertical")
            aux_df = ok

        return aux_df, invalid_records
