from app.quality_result import QualityResult


def test_quality_result():
    result = QualityResult(
        check_name="missing_values",
        column="age",
        affected_count=2,
        total_count=10,
        rate=0.20,
        severity="warning",
        message="Missing values detected",
    )

    assert result.check_name == "missing_values"
    assert result.column == "age"
    assert result.affected_count == 2
    assert result.total_count == 10
    assert result.rate == 0.20
    assert result.severity == "warning"
    assert result.passed is False