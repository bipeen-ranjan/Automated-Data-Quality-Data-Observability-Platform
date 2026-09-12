from app.scoring import (
    calculate_quality_dimensions,
    calculate_quality_score,
)


def test_perfect_quality_score():

    score = calculate_quality_score(
        missing_rate=0,
        duplicate_rate=0,
        invalid_rate=0,
        outlier_rate=0,
    )

    assert score == 100


def test_quality_score_with_issues():

    score = calculate_quality_score(
        missing_rate=0.10,
        duplicate_rate=0.05,
        invalid_rate=0.02,
        outlier_rate=0.10,
    )

    assert 0 < score < 100


def test_quality_score_is_clamped():

    score = calculate_quality_score(
        missing_rate=2,
        duplicate_rate=2,
        invalid_rate=2,
        outlier_rate=2,
    )

    assert score == 0


def test_quality_dimensions():

    dimensions = calculate_quality_dimensions(
        missing_rate=0.10,
        duplicate_rate=0.20,
        invalid_rate=0.05,
        outlier_rate=0.10,
    )

    assert dimensions["completeness"] == 90

    assert dimensions["uniqueness"] == 80

    assert dimensions["validity"] == 95

    assert dimensions["consistency"] == 90