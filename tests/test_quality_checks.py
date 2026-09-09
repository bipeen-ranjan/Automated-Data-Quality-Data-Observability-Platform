from app.data_loader import load_csv
from app.quality_checks import (
    check_missing_values,
    check_duplicates,
    check_invalid_values,
    check_outliers,
)


def test_check_missing_values():
    df = load_csv("data/quality_test_data.csv")

    results = check_missing_values(df)

    age_result = next(
        result for result in results
        if result.column == "age"
    )

    city_result = next(
        result for result in results
        if result.column == "city"
    )

    salary_result = next(
        result for result in results
        if result.column == "salary"
    )

    assert age_result.affected_count == 1
    assert city_result.affected_count == 1
    assert salary_result.affected_count == 1

    assert age_result.check_name == "missing_values"
    assert age_result.passed is False


def test_check_duplicates():
    df = load_csv("data/duplicate_test_data.csv")

    result = check_duplicates(df)

    assert result.check_name == "duplicates"
    assert result.column is None
    assert result.affected_count == 1
    assert result.total_count == 5
    assert result.rate == 0.20
    assert result.passed is False


def test_check_invalid_values():
    df = load_csv("data/invalid_test_data.csv")

    result = check_invalid_values(df)

    assert result.check_name == "invalid_values"
    assert result.column is None
    assert result.affected_count == 3
    assert result.total_count == 5
    assert result.rate == 0.60
    assert result.passed is False


def test_check_outliers():
    df = load_csv("data/outlier_test_data.csv")

    result = check_outliers(df, "salary")

    assert result.check_name == "outliers"
    assert result.column == "salary"
    assert result.affected_count == 1
    assert result.total_count == 9
    assert result.rate == 1 / 9
    assert result.passed is False