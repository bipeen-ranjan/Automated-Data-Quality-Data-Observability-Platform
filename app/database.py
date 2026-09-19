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

DB_NAME = os.getenv(
    "DB_NAME",
    "data_quality_db",
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
    """

    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )