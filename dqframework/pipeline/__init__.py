import enum
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List

import polars as pl

columns = [
    "id"
    "check_id"
    "timestamp"
    "check"
    "level"
    "column"
    "rule"
    "value"
    "rows"
    "violations"
    "pass_rate"
    "pass_threshold"
    "status"
]


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
        self.check_id = str(uuid.uuid4())

    def __call__(
        self, df: pl.DataFrame, *args, **kwargs
    ) -> (pl.DataFrame, pl.DataFrame, pl.DataFrame):
        if not self.validations:
            raise ValueError("No validations added to the check")
        correct_acc = df
        incorrect_acc = pl.DataFrame()

        dq_metrics = pl.DataFrame()
        for validation in self.validations:
            val_id = str(uuid.uuid4())
            rule = validation[0]
            column = validation[1]

            correct, incorrect = rule(correct_acc, *validation[1:])
            correct_acc = correct

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
                        str(*validation[2:]),
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
        pass_rate = float((rows - violations) / rows) if rows > 0 else 0.0
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
                "pass_threshold": [float(self.pass_threshold)],
                "status": ["PASS" if pass_rate >= self.pass_threshold else "FAIL"],
            }
        )


class Pipeline:
    class Status(enum.Enum):
        NOT_EXECUTED = "NOT_EXECUTED"
        EXECUTED = "EXECUTED"

    def __init__(self, checks: List[Check]):
        self.checks = checks
        self.results = None
        self.status = Pipeline.Status.NOT_EXECUTED

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

        self.results = results_df
        self.status = Pipeline.Status.EXECUTED

        return PipelineResults(aux_df, invalid_records, results_df)

    def results_to_csv(self, path: str):
        if self.status == Pipeline.Status.NOT_EXECUTED:
            raise ValueError("Pipeline not executed")

        self.results.write_csv(path)

    def results_to_xlsx(self, path: str):
        if self.status == Pipeline.Status.NOT_EXECUTED:
            raise ValueError("Pipeline not executed")

        self.results.write_excel(path)

    def results_to_json(self, path: str):
        if self.status == Pipeline.Status.NOT_EXECUTED:
            raise ValueError("Pipeline not executed")

        self.results.write_json(path)


@dataclass
class PipelineResults:
    valid_records: pl.DataFrame
    invalid_records: pl.DataFrame
    results: pl.DataFrame
