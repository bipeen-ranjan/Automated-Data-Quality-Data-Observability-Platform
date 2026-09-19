"""
Database operations for analysis runs.
"""

from app.database import get_connection


def create_analysis_run(
    filename,
    rows_count,
    columns_count,
    quality_score,
    completeness,
    uniqueness,
    validity,
    consistency,
):
    """
    Save one dataset analysis result
    into the analysis_runs table.

    Returns:
        The ID of the newly created analysis run.
    """

    query = """
        INSERT INTO analysis_runs (
            filename,
            rows_count,
            columns_count,
            quality_score,
            completeness,
            uniqueness,
            validity,
            consistency
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        RETURNING id;
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    filename,
                    rows_count,
                    columns_count,
                    quality_score,
                    completeness,
                    uniqueness,
                    validity,
                    consistency,
                ),
            )

            analysis_id = cursor.fetchone()[0]

        connection.commit()

        return analysis_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()