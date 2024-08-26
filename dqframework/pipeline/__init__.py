import enum
import uuid
from datetime import datetime
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

    def __init__(
        self,
        level: Level,
        check_name: str,
        pass_threshold: float = 0.9,
    ):
        self.level = level
        self.check_name: str = check_name
        self.validations = []
        self.pass_threshold = pass_threshold
        self.check_id = uuid.uuid4()

    def __call__(
        self, df: pl.DataFrame, *args, **kwargs
    ) -> (pl.DataFrame, pl.DataFrame, pl.DataFrame):
        if not self.validations:
            raise ValueError("No validations added to the check")
        correct_acc = pl.DataFrame()
        incorrect_acc = pl.DataFrame()

        dq_metrics = pl.DataFrame()
        for validation in self.validations:
            val_id = uuid.uuid4()
            (rule, column, value) = validation

            correct, incorrect = rule(df, *validation[1:])
            correct_acc = pl.concat([correct_acc, correct], how="vertical")

            # tag the incorrect with the check_id that failed
            incorrect = incorrect.with_columns(
                pl.lit(str(self.check_id)).alias("check_id"),
                pl.lit(str(val_id)).alias("validation_id"),
            )

            incorrect_acc = pl.concat([incorrect_acc, incorrect], how="vertical")

            dq_metrics = pl.concat(
                [
                    dq_metrics,
                    self.calculate_dq(
                        df,
                        incorrect,
                        column,
                        rule.__name__,
                        str(value),
                        str(val_id),
                    ),
                ]
            )

        return (
            dq_metrics,
            correct_acc,
            incorrect_acc,
        )

    def calculate_dq(
        self,
        original_df: pl.DataFrame,
        incorrect_df: pl.DataFrame,
        column: str,
        rule_name: str,
        value_check: str = "",
        validation_id: str = "",
    ) -> pl.DataFrame:

        rows = original_df.height
        violations = incorrect_df.height
        pass_rate = (rows - violations) / rows
        return pl.DataFrame(
            {
                "id": [validation_id],
                "check_id": [self.check_id],
                "timestamp": [datetime.now()],
                "check": [self.check_name],
                "level": [self.level.value],
                "column": [column],
                "rule": [rule_name],
                "value": [value_check],
                "rows": [rows],
                "violations": [violations],
                "pass_rate": [pass_rate],
                "pass_threshold": [self.pass_threshold],
                "status": ["PASS" if pass_rate >= self.pass_threshold else "FAIL"],
            }
        )


class Pipeline:
    def __init__(self, checks: List[Check]):
        self.checks = checks

    def execute(self, df: pl.DataFrame):
        if not self.checks:
            raise ValueError("No checks added to the pipeline")

        aux_df = df
        invalid_records = pl.DataFrame()
        results_df = pl.DataFrame()
        for check in self.checks:
            (results, ok, notok) = check(aux_df)

            invalid_records = pl.concat([invalid_records, notok], how="vertical")
            results_df = pl.concat([results_df, results], how="vertical")
            aux_df = ok

        return aux_df, invalid_records, results_df
