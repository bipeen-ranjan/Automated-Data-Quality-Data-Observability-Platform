from app.quality_checks import (
    check_missing_values,
    check_duplicates,
    check_invalid_values,
    check_outliers,
)


def run_quality_checks(df):
    """
    Run all available data-quality checks on a DataFrame.
    """

    # 1. Missing-value checks
    missing_results = check_missing_values(df)

    # 2. Duplicate check
    duplicate_result = check_duplicates(df)

    # 3. Invalid-value check
    invalid_count = check_invalid_values(df)

    # 4. Outlier checks for numerical columns
    numeric_columns = df.select_dtypes(include="number").columns

    outlier_count = 0

    for column in numeric_columns:
        outlier_count += check_outliers(df, column)

    # 5. Return all quality-check results
    return {
        "missing_results": missing_results,
        "duplicate_result": duplicate_result,
        "invalid_count": invalid_count,
        "outlier_count": outlier_count,
    }