from app.database import get_connection


def test_database_connection():

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT current_database();"
            )

            database_name = cursor.fetchone()[0]

        assert database_name == "data_quality_db"

    finally:

        connection.close()