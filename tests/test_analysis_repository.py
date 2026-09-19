from app.repositories.analysis_repository import (
    create_analysis_run,
)


def test_create_analysis_run():

    analysis_id = create_analysis_run(
        filename="test_dataset.csv",
        rows_count=10,
        columns_count=3,
        quality_score=95.50,
        completeness=98.00,
        uniqueness=100.00,
        validity=96.00,
        consistency=90.00,
    )

    assert isinstance(
        analysis_id,
        int,
    )

    assert analysis_id > 0