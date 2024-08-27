from datetime import datetime

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


def has_max(df: pl.DataFrame, column: str, value: int) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has a maximum value of value

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param value: maximum value to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column) <= value)
    incorrect = df.filter(pl.col(column) > value)

    return correct, incorrect


def has_string_length(
    df: pl.DataFrame, column: str, value: int
) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has a string length of value

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param value: length to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column).str.len_chars() == value)
    incorrect = df.filter(pl.col(column).str.len_chars() != value)

    return correct, incorrect


def has_string_length_between(
    df: pl.DataFrame, column: str, min_value: int, max_value: int
) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has a string length between min_value and max_value

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param min_value: minimum length to check
    :param max_value: maximum length to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(
        (pl.col(column).str.len_chars() >= min_value)
        & (pl.col(column).str.len_chars() <= max_value)
    )
    incorrect = df.filter(
        (pl.col(column).str.len_chars() < min_value)
        | (pl.col(column).str.len_chars() > max_value)
    )

    return correct, incorrect


def has_between(
    df: pl.DataFrame, column: str, min_value: int, max_value: int
) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has a value between min_value and max_value

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param min_value: minimum value to check
    :param max_value: maximum value to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter((pl.col(column) >= min_value) & (pl.col(column) <= max_value))
    incorrect = df.filter((pl.col(column) < min_value) | (pl.col(column) > max_value))

    return correct, incorrect


def has_max_length(
    df: pl.DataFrame, column: str, value: int
) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has a maximum string length of value

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param value: maximum length to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column).str.len_chars() <= value)
    incorrect = df.filter(pl.col(column).str.len_chars() > value)

    return correct, incorrect


def is_complete(df: pl.DataFrame, column: str) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column is complete

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column).is_not_null())
    incorrect = df.filter(pl.col(column).is_null())

    return correct, incorrect


def is_unique(df: pl.DataFrame, column: str) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has unique values

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column).is_unique())
    incorrect = df.filter(~pl.col(column).is_unique())

    return correct, incorrect


def is_composite_key(df: pl.DataFrame, columns: list) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame has a composite key

    Parameters
    :param df: DataFrame
    :param columns: list of columns to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(df.select(columns).is_unique())
    incorrect = df.filter(~df.select(columns).is_unique())

    return correct, incorrect


def no_future_dates(df: pl.DataFrame, column: str, date: datetime = datetime.today()):
    """
    Check if a DataFrame column has no future dates

    :param df: Dataframe
    :param column: name of the column to check
    :param date: datetime.datetime (default is right now)
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column) <= pl.lit(datetime.now()))
    incorrect = df.filter(pl.col(column) > pl.lit(datetime.now()))

    return correct, incorrect


def is_in(df: pl.DataFrame, column: str, values: list) -> (pl.DataFrame, pl.DataFrame):
    """
    Check if a DataFrame column has values in a list

    Parameters
    :param df: DataFrame
    :param column: name of the column to check
    :param values: list of values to check
    :return: (pl.DataFrame, pl.DataFrame) - correct, incorrect
    """

    correct = df.filter(pl.col(column).is_in(values))
    incorrect = df.filter(~pl.col(column).is_in(values))

    return correct, incorrect
