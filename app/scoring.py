"""
Data quality scoring module.

Calculates an explainable overall quality score
using independent quality dimensions.
"""


DEFAULT_WEIGHTS = {
    "completeness": 0.40,
    "uniqueness": 0.20,
    "validity": 0.25,
    "consistency": 0.15,
}


def _clamp_rate(rate):
    """
    Keep a rate between 0 and 1.
    """

    return min(
        max(float(rate), 0.0),
        1.0,
    )


def calculate_quality_score(
    missing_rate,
    duplicate_rate,
    invalid_rate,
    outlier_rate,
):
    """
    Calculate an overall data quality score.

    Dimensions:

        Completeness = 1 - missing rate
        Uniqueness   = 1 - duplicate rate
        Validity     = 1 - invalid rate
        Consistency  = 1 - outlier rate

    Default weights:

        Completeness = 40%
        Uniqueness   = 20%
        Validity     = 25%
        Consistency  = 15%

    Returns:
        Overall quality score between 0 and 100.
    """

    missing_rate = _clamp_rate(
        missing_rate
    )

    duplicate_rate = _clamp_rate(
        duplicate_rate
    )

    invalid_rate = _clamp_rate(
        invalid_rate
    )

    outlier_rate = _clamp_rate(
        outlier_rate
    )

    completeness = (
        1 - missing_rate
    )

    uniqueness = (
        1 - duplicate_rate
    )

    validity = (
        1 - invalid_rate
    )

    consistency = (
        1 - outlier_rate
    )

    score = (
        completeness
        * DEFAULT_WEIGHTS["completeness"]
        +
        uniqueness
        * DEFAULT_WEIGHTS["uniqueness"]
        +
        validity
        * DEFAULT_WEIGHTS["validity"]
        +
        consistency
        * DEFAULT_WEIGHTS["consistency"]
    )

    return round(
        score * 100,
        2,
    )


def calculate_quality_dimensions(
    missing_rate,
    duplicate_rate,
    invalid_rate,
    outlier_rate,
):
    """
    Calculate individual quality dimensions.

    Returns:
        Dictionary containing dimension scores
        between 0 and 100.
    """

    missing_rate = _clamp_rate(
        missing_rate
    )

    duplicate_rate = _clamp_rate(
        duplicate_rate
    )

    invalid_rate = _clamp_rate(
        invalid_rate
    )

    outlier_rate = _clamp_rate(
        outlier_rate
    )

    return {
        "completeness": round(
            (1 - missing_rate) * 100,
            2,
        ),
        "uniqueness": round(
            (1 - duplicate_rate) * 100,
            2,
        ),
        "validity": round(
            (1 - invalid_rate) * 100,
            2,
        ),
        "consistency": round(
            (1 - outlier_rate) * 100,
            2,
        ),
    }