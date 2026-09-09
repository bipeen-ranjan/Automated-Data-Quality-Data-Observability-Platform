from app.data_loader import load_csv

from app.profiler import profile_data

from app.quality_checks import (
    check_missing_values,
    check_duplicates,
    check_invalid_values,
    check_outliers,
)

from app.scoring import calculate_quality_score


def analyze_dataset(file_path):
    """
    Run the complete data quality analysis pipeline.
    """

    # 1. Load the dataset
    df = load_csv(file_path)

    # 2. Generate dataset profile
    profile = profile_data(df)

    # 3. Run quality checks
    missing_values = check_missing_values(df)
    duplicate_count = check_duplicates(df)
    invalid_count = check_invalid_values(df)

    # 4. Detect outliers in all numerical columns
    numeric_columns = df.select_dtypes(include="number").columns

    outlier_count = 0

    for column in numeric_columns:
        outlier_count += check_outliers(df, column)

    # 5. Calculate issue rates
    total_rows = len(df)

    missing_count = sum(missing_values.values())

    missing_rate = missing_count / total_rows
    duplicate_rate = duplicate_count / total_rows
    invalid_rate = invalid_count / total_rows
    outlier_rate = outlier_count / total_rows

    # 6. Calculate overall quality score
    quality_score = calculate_quality_score(
        missing_rate=missing_rate,
        duplicate_rate=duplicate_rate,
        invalid_rate=invalid_rate,
        outlier_rate=outlier_rate,
    )

    # 7. Return complete analysis
    return {
        "profile": profile,
        "quality": {
            "missing_values": missing_values,
            "duplicate_count": duplicate_count,
            "invalid_count": invalid_count,
            "outlier_count": outlier_count,
            "quality_score": quality_score,
        },
    }

def test_analyzer_detects_outlier():
    result = analyze_dataset("data/outlier_test_data.csv")

    assert result["quality"]["outlier_count"] >= 1