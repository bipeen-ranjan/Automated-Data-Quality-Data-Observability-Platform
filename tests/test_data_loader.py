import pandas as pd
import pytest

from app.data_loader import load_dataset


def test_load_csv():

    df = load_dataset(
        "data/sample_data.csv"
    )

    assert isinstance(
        df,
        pd.DataFrame,
    )

    assert len(df) > 0


def test_load_unsupported_file():

    with pytest.raises(ValueError):

        load_dataset(
            "data/sample_data.txt"
        )