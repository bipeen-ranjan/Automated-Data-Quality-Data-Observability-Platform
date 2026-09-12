"""
Generic dataset loader.

Supports CSV and Excel files and returns
a Pandas DataFrame.
"""

import os

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
}


def load_dataset(file_path):
    """
    Load a CSV or Excel dataset.

    Parameters:
        file_path: Path to the dataset.

    Returns:
        Pandas DataFrame.

    Raises:
        ValueError: If the file format is unsupported
        or the dataset cannot be loaded.
    """

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            "Unsupported file format. "
            "Supported formats: CSV, XLSX, XLS."
        )

    try:

        if extension == ".csv":

            return pd.read_csv(file_path)

        return pd.read_excel(file_path)

    except Exception as e:

        raise ValueError(
            f"Unable to load dataset: {e}"
        )


def load_csv(file_path):
    """
    Backward-compatible CSV loader.

    This function is retained so existing code and
    tests using load_csv() continue to work.

    New code should use load_dataset().
    """

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension != ".csv":

        raise ValueError(
            "load_csv() only supports CSV files."
        )

    return load_dataset(file_path)