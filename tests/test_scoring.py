from app.scoring import calculate_quality_score


def test_calculate_quality_score():
    score = calculate_quality_score(
        missing_rate=0.02,
        duplicate_rate=0.01,
        invalid_rate=0.01,
        outlier_rate=0.01,
    )

    assert score == 95