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


def has_string_pattern(
    df: pl.DataFrame, column: str, value: str
) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has a string pattern

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param value: pattern to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column).str.contains(value))
    incorrect = df.filter(~pl.col(column).str.contains(value))

    return correct, incorrect


def has_date_pattern(
    df: pl.DataFrame, column: str, value: str = "%Y-%m-%d"
) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has a date pattern

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param value: pattern to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column).str.to_date(value, strict=False).is_not_null())
    incorrect = df.filter(pl.col(column).str.to_date(value, strict=False).is_null())

    return correct, incorrect
