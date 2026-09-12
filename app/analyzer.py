"""
Complete dataset analysis pipeline.
"""

from app.data_loader import load_dataset
from app.profiler import profile_data
from app.quality_engine import run_quality_checks
from app.scoring import (
    calculate_quality_dimensions,
    calculate_quality_score,
)


def analyze_dataset(
    file_path,
    validation_rules=None,
):
    """
    Run the complete data-quality analysis pipeline.
    """

    df = load_dataset(file_path)

    profile = profile_data(df)

    quality_results = run_quality_checks(
        df,
        validation_rules=validation_rules,
    )

    missing_results = quality_results[
        "missing_results"
    ]

    duplicate_result = quality_results[
        "duplicate_result"
    ]

    invalid_results = quality_results[
        "invalid_results"
    ]

    outlier_results = quality_results[
        "outlier_results"
    ]

    column_types = quality_results[
        "column_types"
    ]

    # --------------------------------------------------
    # Issue counts
    # --------------------------------------------------

    missing_count = sum(
        result.affected_count
        for result in missing_results
    )

    duplicate_count = (
        duplicate_result.affected_count
    )

    invalid_count = sum(
        result.affected_count
        for result in invalid_results
    )

    outlier_count = sum(
        result.affected_count
        for result in outlier_results
    )

    # --------------------------------------------------
    # Dataset dimensions
    # --------------------------------------------------

    total_rows = len(df)

    total_columns = len(df.columns)

    total_cells = (
        total_rows * total_columns
    )

    # --------------------------------------------------
    # Completeness
    #
    # Missing values are cell-level issues.
    # Therefore the denominator must be total cells.
    # --------------------------------------------------

    missing_rate = (
        missing_count / total_cells
        if total_cells > 0
        else 0
    )

    # --------------------------------------------------
    # Uniqueness
    #
    # Duplicate rows are row-level issues.
    # --------------------------------------------------

    duplicate_rate = (
        duplicate_count / total_rows
        if total_rows > 0
        else 0
    )

    # --------------------------------------------------
    # Validity
    #
    # Configured validation currently produces
    # column-level invalid counts.
    #
    # For now, use total rows as the denominator.
    # This will be refined when the validation engine
    # supports richer rule-level metrics.
    # --------------------------------------------------

    invalid_rate = (
        invalid_count / total_rows
        if total_rows > 0
        else 0
    )

    # --------------------------------------------------
    # Consistency
    #
    # Outliers are calculated independently for each
    # numeric column.
    #
    # Therefore the denominator should be the total
    # number of numeric observations.
    # --------------------------------------------------

    numeric_columns = [
        column
        for column, column_type
        in column_types.items()
        if column_type == "numeric"
    ]

    numeric_observations = sum(
        int(df[column].notna().sum())
        for column in numeric_columns
    )

    outlier_rate = (
        outlier_count / numeric_observations
        if numeric_observations > 0
        else 0
    )

    # --------------------------------------------------
    # Quality score
    # --------------------------------------------------

    quality_score = calculate_quality_score(
        missing_rate=missing_rate,
        duplicate_rate=duplicate_rate,
        invalid_rate=invalid_rate,
        outlier_rate=outlier_rate,
    )

    quality_dimensions = (
        calculate_quality_dimensions(
            missing_rate=missing_rate,
            duplicate_rate=duplicate_rate,
            invalid_rate=invalid_rate,
            outlier_rate=outlier_rate,
        )
    )

    return {
        "profile": profile,

        "quality": {
            "missing_results": missing_results,

            "duplicate_result": duplicate_result,

            "invalid_results": invalid_results,

            "invalid_result": quality_results[
                "invalid_result"
            ],

            "outlier_results": outlier_results,

            "column_types": column_types,

            "quality_score": quality_score,

            "quality_dimensions": (
                quality_dimensions
            ),

            # Useful for dashboard and future
            # observability features.
            "metrics": {
                "missing_count": missing_count,
                "duplicate_count": duplicate_count,
                "invalid_count": invalid_count,
                "outlier_count": outlier_count,
                "total_cells": total_cells,
                "numeric_observations": (
                    numeric_observations
                ),
                "missing_rate": missing_rate,
                "duplicate_rate": duplicate_rate,
                "invalid_rate": invalid_rate,
                "outlier_rate": outlier_rate,
            },
        },
    }