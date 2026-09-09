from app.data_loader import load_csv
from app.quality_engine import run_quality_checks


def test_run_quality_checks():
    df = load_csv("data/quality_test_data.csv")

    results = run_quality_checks(df)

    assert "missing_results" in results
    assert "duplicate_result" in results
    assert "invalid_count" in results
    assert "outlier_count" in results

    assert len(results["missing_results"]) == 5

    assert results["duplicate_result"].affected_count == 0
    assert results["invalid_count"] == 0