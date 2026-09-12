"""
Main data-quality engine.
"""

from app.column_classifier import classify_dataframe
from app.quality_checks import (
    check_missing_values,
    check_duplicates,
    check_invalid_values,
    check_outliers,
)
from app.quality_result import QualityResult


def _create_invalid_summary(
    invalid_results,
    total_rows,
):
    """
    Create one summary QualityResult from
    multiple invalid-value results.
    """

    invalid_count = sum(
        result.affected_count
        for result in invalid_results
    )

    rate = (
        invalid_count / total_rows
        if total_rows > 0
        else 0
    )

    if rate == 0:
        severity = "info"
    elif rate <= 0.05:
        severity = "warning"
    elif rate <= 0.20:
        severity = "error"
    else:
        severity = "critical"

    if invalid_count == 0:

        message = "No invalid values detected."

    else:

        message = (
            f"{invalid_count} invalid value(s) "
            "detected across configured columns."
        )

    return QualityResult(
        check_name="invalid_values",
        column=None,
        affected_count=invalid_count,
        total_count=total_rows,
        rate=rate,
        severity=severity,
        message=message,
    )


def run_quality_checks(
    df,
    validation_rules=None,
):
    """
    Run all data-quality checks.

    The engine automatically classifies columns
    before selecting statistical checks.
    """

    # -------------------------------------------------
    # 1. Missing values
    # -------------------------------------------------

    missing_results = check_missing_values(df)

    # -------------------------------------------------
    # 2. Duplicate rows
    # -------------------------------------------------

    duplicate_result = check_duplicates(df)

    # -------------------------------------------------
    # 3. Column classification
    # -------------------------------------------------

    column_types = classify_dataframe(df)

    # -------------------------------------------------
    # 4. Invalid values
    # -------------------------------------------------

    if validation_rules is None:

        # Preserve existing behavior
        invalid_result = check_invalid_values(df)

        invalid_results = [invalid_result]

    else:

        invalid_results = check_invalid_values(
            df,
            validation_rules,
        )

        invalid_result = _create_invalid_summary(
            invalid_results,
            len(df),
        )

    # -------------------------------------------------
    # 5. Outlier detection
    # -------------------------------------------------

    outlier_results = []

    for column, column_type in column_types.items():

        # Only continuous numeric columns
        # are considered for IQR outlier detection.
        if column_type != "numeric":
            continue

        result = check_outliers(
            df,
            column,
        )

        outlier_results.append(result)

    # -------------------------------------------------
    # 6. Return results
    # -------------------------------------------------

    return {
        "missing_results": missing_results,

        "duplicate_result": duplicate_result,

        "invalid_results": invalid_results,

        # Kept for backward compatibility
        "invalid_result": invalid_result,

        "outlier_results": outlier_results,

        # New information
        "column_types": column_types,
    }