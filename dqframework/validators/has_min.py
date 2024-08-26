import polars as pl


def has_min(df: pl.DataFrame, column: str, value: int) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has a minimum value of value

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param value: minimum value to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column) >= value)
    incorrect = df.filter(pl.col(column) < value)

    return correct, incorrect
