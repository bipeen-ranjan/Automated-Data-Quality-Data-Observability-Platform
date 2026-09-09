from app.data_loader import load_csv
from app.profiler import profile_data


def test_profile_data():
    df = load_csv("data/sample_data.csv")

    profile = profile_data(df)

    assert profile["rows"] == 8
    assert profile["columns"] == 5
    assert "age" in profile["column_names"]
    assert profile["missing_values"]["age"] == 0