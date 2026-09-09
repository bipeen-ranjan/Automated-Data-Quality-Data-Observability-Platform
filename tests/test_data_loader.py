from app.data_loader import load_csv


def test_load_csv():
    file_path = "data/sample_data.csv"

    df = load_csv(file_path)

    assert df is not None
    assert len(df) == 8
    assert len(df.columns) == 5