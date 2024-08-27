import polars as pl

from dqframework.pipeline import Pipeline, Check
from dqframework.validators import has_string_pattern

if __name__ == "__main__":
    # Create a dataframe
    df = pl.DataFrame(
        {
            "Name": ["Hannah", "Bob", "Alice"],
            "Job": ["Data Engineer", "Data Scientist", "Business Analyst"],
        }
    )

    # Check #1
    check1 = Check(Check.Level.ERROR, "Job starts with Data or Business", 1.0)
    check1.validations.append([has_string_pattern, "Job", r"(Data \w+)|(Business \w+)"])

    # Check 2
    check2 = Check(Check.Level.INFO, "Name starts with A")
    check2.validations.append([has_string_pattern, "Name", "A.+"])

    # Create a pipeline
    pipeline = Pipeline(checks=[check1, check2])
    # Print the result

    pipeline.execute(df)

    pipeline.results_to_csv("pipeline_results.csv")
