from app.analyzer import analyze_dataset


def test_analyze_dataset():
    result = analyze_dataset("data/sample_data.csv")

    assert "profile" in result
    assert "quality" in result

    assert result["profile"]["rows"] == 8
    assert result["profile"]["columns"] == 5

    assert "quality_score" in result["quality"]
    assert 0 <= result["quality"]["quality_score"] <= 100

    assert "outlier_results" in result["quality"]


def test_analyzer_detects_outlier():
    result = analyze_dataset("data/outlier_test_data.csv")

    outlier_results = result["quality"]["outlier_results"]

    total_outliers = sum(
        item.affected_count
        for item in outlier_results
    )

    assert total_outliers >= 1


def test_analyzer_calculates_valid_rates():

    result = analyze_dataset(
        "data/quality_test_data.csv"
    )

    metrics = result["quality"]["metrics"]

    assert metrics["total_cells"] > 0

    assert (
        0 <= metrics["missing_rate"] <= 1
    )

    assert (
        0 <= metrics["duplicate_rate"] <= 1
    )

    assert (
        0 <= metrics["invalid_rate"] <= 1
    )

    assert (
        0 <= metrics["outlier_rate"] <= 1
    )    