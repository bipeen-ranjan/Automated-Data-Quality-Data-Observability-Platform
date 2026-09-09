def calculate_quality_score(
    missing_rate,
    duplicate_rate,
    invalid_rate,
    outlier_rate,
):
    """
    Calculate data quality score from issue rates.

    Each rate should be between 0 and 1.
    """

    total_issue_rate = (
        missing_rate
        + duplicate_rate
        + invalid_rate
        + outlier_rate
    )

    score = 100 - (total_issue_rate * 100)

    return max(round(score, 2), 0)