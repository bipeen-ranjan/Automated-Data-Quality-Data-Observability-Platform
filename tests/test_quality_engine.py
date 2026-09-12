from app.quality_engine import run_quality_checks
from app.data_loader import load_csv


def test_run_quality_checks():

    df = load_csv(
        "data/quality_test_data.csv"
    )

    results = run_quality_checks(df)

    assert "missing_results" in results
    assert "duplicate_result" in results
    assert "invalid_result" in results
    assert "invalid_results" in results
    assert "outlier_results" in results
    assert "column_types" in results

    # ---------------------------------------------
    # Missing values
    # ---------------------------------------------

    assert len(
        results["missing_results"]
    ) == 5

    # ---------------------------------------------
    # Duplicates
    # ---------------------------------------------

    assert (
        results["duplicate_result"].affected_count
        == 0
    )

    # ---------------------------------------------
    # Invalid values
    # ---------------------------------------------

    assert (
        results["invalid_result"].affected_count
        == 0
    )

    # ---------------------------------------------
    # Column classification
    # ---------------------------------------------

    column_types = results["column_types"]

    assert (
        column_types["customer_id"]
        == "identifier"
    )

    assert (
        column_types["age"]
        == "numeric"
    )

    assert (
        column_types["salary"]
        == "numeric"
    )

    # ---------------------------------------------
    # Outlier detection
    # ---------------------------------------------

    # customer_id is an identifier and should NOT
    # be treated as a continuous numeric variable.
    #
    # Therefore only age and salary are checked.

    assert len(
        results["outlier_results"]
    ) == 2