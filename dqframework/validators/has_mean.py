import polars as pl

from .base_validator import Validator
from .comparisons_operator import ComparisonsOperator


class HasMean(Validator):
    """
    Check if a DataFrame column has an average value of value

    Parameters
    :param column: name of the column to check
    :param value: average value to check
    :param comparison_op: comparison operator to use
    """

    def __init__(self, column: str, value: int, comparison_op: ComparisonsOperator):
        super().__init__(column, value)

        if not isinstance(comparison_op, ComparisonsOperator):
            raise ValueError("comparison_op must be a ComparisonsOperator")
        self.comparison_op = comparison_op

    def execute(self, df: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
        expr = eval(f"pl.col(self.column).mean() {self.comparison_op} {self.value}")
        correct = df.filter(expr)
        incorrect = df.filter(~expr)

        return correct, incorrect
