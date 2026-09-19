import os

from app.database import get_connection


def test_database_connection():

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT current_database();"
            )

            database_name = cursor.fetchone()[0]

        expected_database = os.getenv(
            "DB_NAME"
        )

        assert database_name == expected_database

        assert database_name == "data_quality_test_db"

    finally:

        connection.close()