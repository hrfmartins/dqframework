# dqframework is a Python package that provides a framework for data quality assessment and monitoring.

This package is designed with polars in mind, but in the future it might get expanded.

## Another framework?

This framework is designed to be used in a similar way to many others, but it has been designed with some goals in mind:

- **Observability**: The framework should provide a way to monitor the data quality of a dataset in a way that is easy
  to understand and to act upon.
- **Extensibility**: The framework should be easy to extend with new checks and new ways to monitor the data quality.
- **Performance**: The framework should be able to handle large datasets and provide a way to monitor the data quality
  of these datasets in a performant way.
- **Ease of use**: The framework should be easy to use and to understand, so that it can be used by data engineers, data
  scientists, and other data professionals.
- **Monitoring and Reporting**: The framework should provide a way to monitor the data quality of a dataset over time
  and to report on the data quality of the dataset.

## How to use it?

This framework is centered around three main concepts:

- Pipeline: A pipeline is an object that comprises multiple Checks, and is responsible for running these checks on a
  dataframe.
- Check: A check is an object that comprises multiple Validators, and is responsible for checking a certain set of
  properties of a dataframe. It has severity levels, and can be used to monitor the data quality of a dataset.
- Validator: A validator is a function that is responsible for validating a certain property of a dataframe

## Installation

To install the package, you can use pip:

```bash
pip install dqframework
```
