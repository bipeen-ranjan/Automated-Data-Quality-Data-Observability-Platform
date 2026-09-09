from app.data_loader import load_csv
from app.quality_checks import (
    check_missing_values,
    check_duplicates,
    check_invalid_values,
    check_outliers,
)


def test_check_missing_values():
    df = load_csv("data/quality_test_data.csv")

    missing_values = check_missing_values(df)

    assert missing_values["age"] == 1
    assert missing_values["city"] == 1
    assert missing_values["salary"] == 1

def test_check_invalid_values():
    df = load_csv("data/invalid_test_data.csv")

    invalid_count = check_invalid_values(df)

    assert invalid_count == 3    


def test_check_outliers():
    df = load_csv("data/outlier_test_data.csv")

    outlier_count = check_outliers(df, "salary")

    assert outlier_count == 1

    

def test_check_duplicates():
    df = load_csv("data/duplicate_test_data.csv")

    duplicate_count = check_duplicates(df)

    assert duplicate_count == 1

