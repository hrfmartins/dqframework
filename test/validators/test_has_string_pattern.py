import polars as pl

from dqframework.validators import HasStrPattern


def test_has_string_pattern():
    df = pl.DataFrame({"a": ["a", "b", "c"], "b": [4, 5, 6]})

    correct, incorrect = HasStrPattern("a", r"\w").execute(df)

    assert correct.height == 3
    assert incorrect.height == 0


def test_has_two_invalids():
    df = pl.DataFrame({"a": ["a", "2", "c"], "b": [4, 5, 6]})

    correct, incorrect = HasStrPattern("a", r"\d").execute(df)

    assert correct.height == 1
    assert incorrect.height == 2


def test_complex_regex():
    df = pl.DataFrame({"name": ["John", "Mary", "Clark"], "Number": [4, 5, 6]})

    correct, incorrect = HasStrPattern("name", r"^C[a-zA-Z]+").execute(df)

    assert correct.height == 1
    assert incorrect.height == 2
    assert incorrect["name"].to_list() == ["John", "Mary"]
