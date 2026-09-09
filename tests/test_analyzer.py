from app.analyzer import analyze_dataset


def test_analyze_dataset():
    result = analyze_dataset("data/sample_data.csv")

    assert "profile" in result
    assert "quality" in result

    assert result["profile"]["rows"] == 8
    assert result["profile"]["columns"] == 5

    assert "quality_score" in result["quality"]
    assert 0 <= result["quality"]["quality_score"] <= 100


def test_analyzer_detects_outlier():
    result = analyze_dataset("data/outlier_test_data.csv")

    assert result["quality"]["outlier_count"] >= 1