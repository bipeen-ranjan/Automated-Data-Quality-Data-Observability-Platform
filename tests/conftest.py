"""
Pytest configuration.

All automated tests use the dedicated
PostgreSQL test database instead of the
development database.
"""

import os


# Use the dedicated test database during pytest runs.
os.environ["DB_NAME"] = "data_quality_test_db"