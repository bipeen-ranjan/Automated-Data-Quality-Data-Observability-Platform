from app.data_loader import load_csv
from app.profiler import profile_data
from app.quality_engine import run_quality_checks
from app.scoring import calculate_quality_score


def analyze_dataset(file_path):
    """
    Run the complete data quality analysis pipeline.
    """

    # 1. Load dataset
    df = load_csv(file_path)

    # 2. Generate profile
    profile = profile_data(df)

    # 3. Run quality checks
    quality_results = run_quality_checks(df)

    # 4. Extract results
    missing_results = quality_results["missing_results"]
    duplicate_result = quality_results["duplicate_result"]
    invalid_result = quality_results["invalid_result"]
    outlier_results = quality_results["outlier_results"]

    # 5. Calculate issue counts
    missing_count = sum(
        result.affected_count
        for result in missing_results
    )

    duplicate_count = duplicate_result.affected_count
    invalid_count = invalid_result.affected_count

    outlier_count = sum(
        result.affected_count
        for result in outlier_results
    )

    # 6. Calculate issue rates
    total_rows = len(df)

    missing_rate = (
        missing_count / total_rows
        if total_rows > 0
        else 0
    )

    duplicate_rate = (
        duplicate_count / total_rows
        if total_rows > 0
        else 0
    )

    invalid_rate = (
        invalid_count / total_rows
        if total_rows > 0
        else 0
    )

    outlier_rate = (
        outlier_count / total_rows
        if total_rows > 0
        else 0
    )

    # 7. Calculate quality score
    quality_score = calculate_quality_score(
        missing_rate=missing_rate,
        duplicate_rate=duplicate_rate,
        invalid_rate=invalid_rate,
        outlier_rate=outlier_rate,
    )

    # 8. Return complete analysis
    return {
        "profile": profile,
        "quality": {
            "missing_results": missing_results,
            "duplicate_result": duplicate_result,
            "invalid_result": invalid_result,
            "outlier_results": outlier_results,
            "quality_score": quality_score,
        },
    }