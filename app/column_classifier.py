"""
Automatic column-type detection for uploaded datasets.
"""

import re

import pandas as pd


# =========================================================
# COLUMN NAME PATTERNS
# =========================================================

IDENTIFIER_PATTERNS = [
    "id",
    "identifier",
    "uuid",
]


CATEGORICAL_PATTERNS = [
    "category",
    "type",
    "class",
    "status",
    "gender",
    "sex",
    "rating",
    "grade",
    "level",
    "group",
    "flag",
    "boolean",
]


# Explicit names that usually represent categorical
# or label-like fields rather than free-form documents.
CATEGORICAL_EXACT_NAMES = [
    "name",
    "department",
    "state",
    "city",
    "country",
    "region",
    "occupation",
    "job",
    "role",
]


DATE_PATTERNS = [
    "date",
    "datetime",
    "timestamp",
    "time",
]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def _normalized_name(column):
    """
    Normalize a column name.

    Examples:

        Customer ID -> customerid
        Order_Date  -> orderdate
        PClass      -> pclass
    """

    return re.sub(
        r"[^a-z0-9]",
        "",
        str(column).lower(),
    )


def _looks_like_identifier(column):
    """
    Determine whether a column name indicates
    an identifier.

    We intentionally do not use uniqueness alone.
    """

    normalized = _normalized_name(column)

    for pattern in IDENTIFIER_PATTERNS:

        if normalized == pattern:
            return True

        if normalized.endswith(pattern):
            return True

    return False


def _looks_like_categorical_name(column):
    """
    Determine whether the column name strongly
    indicates a categorical variable.
    """

    normalized = _normalized_name(column)

    # Exact semantic names
    if normalized in CATEGORICAL_EXACT_NAMES:
        return True

    # General categorical keywords
    for pattern in CATEGORICAL_PATTERNS:

        if pattern in normalized:
            return True

    return False


def _looks_like_date(column, series):
    """
    Determine whether a column is likely to contain
    dates or timestamps.
    """

    normalized = _normalized_name(column)

    # -------------------------------------------------
    # Column-name based detection
    # -------------------------------------------------

    for pattern in DATE_PATTERNS:

        if pattern in normalized:
            return True

    # -------------------------------------------------
    # Already a datetime dtype
    # -------------------------------------------------

    if pd.api.types.is_datetime64_any_dtype(series):
        return True

    # -------------------------------------------------
    # String/object date detection
    # -------------------------------------------------

    if (
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_string_dtype(series)
    ):

        non_null = series.dropna()

        if len(non_null) == 0:
            return False

        sample = non_null.head(100)

        try:

            parsed = pd.to_datetime(
                sample,
                errors="coerce",
                format="mixed",
            )

            valid_ratio = (
                parsed.notna().mean()
            )

            if valid_ratio >= 0.90:
                return True

        except Exception:

            return False

    return False


def _looks_like_binary(series):
    """
    Detect binary numerical columns.

    Example:

        Survived = 0 / 1
    """

    if not pd.api.types.is_numeric_dtype(series):
        return False

    non_null = series.dropna()

    if len(non_null) == 0:
        return False

    unique_values = set(
        non_null.unique()
    )

    return unique_values.issubset(
        {0, 1}
    )


# =========================================================
# MAIN CLASSIFIER
# =========================================================

def classify_column(column, series):
    """
    Classify one DataFrame column.

    Possible classifications:

        identifier
        numeric
        categorical
        datetime
        text
    """

    # -------------------------------------------------
    # 1. Identifier
    # -------------------------------------------------

    if _looks_like_identifier(column):

        return "identifier"

    # -------------------------------------------------
    # 2. Date / Time
    # -------------------------------------------------

    if _looks_like_date(
        column,
        series,
    ):

        return "datetime"

    # -------------------------------------------------
    # 3. Boolean
    # -------------------------------------------------

    if pd.api.types.is_bool_dtype(series):

        return "categorical"

    # -------------------------------------------------
    # 4. Explicit categorical column name
    # -------------------------------------------------

    if _looks_like_categorical_name(column):

        return "categorical"

    # -------------------------------------------------
    # 5. Binary numerical column
    # -------------------------------------------------

    if _looks_like_binary(series):

        return "categorical"

    # -------------------------------------------------
    # 6. Numeric
    # -------------------------------------------------

    if pd.api.types.is_numeric_dtype(series):

        return "numeric"

    # -------------------------------------------------
    # 7. String / Object
    # -------------------------------------------------

    if (
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_string_dtype(series)
    ):

        non_null = series.dropna()

        if len(non_null) == 0:

            return "categorical"

        unique_ratio = (
            non_null.nunique()
            / len(non_null)
        )

        # Low-cardinality string columns are
        # generally categorical.

        if unique_ratio <= 0.50:

            return "categorical"

        # High-cardinality string fields are generally
        # free-form text.

        return "text"

    # -------------------------------------------------
    # 8. Fallback
    # -------------------------------------------------

    return "text"


def classify_dataframe(df):
    """
    Classify every column in a DataFrame.

    Returns:

        {
            "column_name": "classification"
        }
    """

    classifications = {}

    for column in df.columns:

        classifications[column] = classify_column(
            column,
            df[column],
        )

    return classifications