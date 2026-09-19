"""
PostgreSQL database connection.

This module provides a connection to the
project's PostgreSQL database.
"""

import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.getenv(
    "DB_HOST",
    "localhost",
)

DB_PORT = os.getenv(
    "DB_PORT",
    "5432",
)

DB_USER = os.getenv(
    "DB_USER",
    "postgres",
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
)


def get_connection():
    """
    Create and return a PostgreSQL database connection.

    The database name is read from the environment
    each time a connection is created.
    """

    database_name = os.getenv(
        "DB_NAME",
        "data_quality_db",
    )

    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=database_name,
        user=DB_USER,
        password=DB_PASSWORD,
    )