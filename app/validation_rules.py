"""
Generic validation rules for different data types.
"""


def validate_numeric_range(df, column, min_value=None, max_value=None):
    """
    Check whether numeric values fall within an allowed range.

    Parameters:
        df: Pandas DataFrame
        column: Column to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Boolean Series where True means the value is invalid.
    """

    invalid = df[column].notna()

    if min_value is not None:
        invalid &= df[column] < min_value

    if max_value is not None:
        invalid |= (
            df[column].notna()
            & (df[column] > max_value)
        )

    return invalid


def validate_allowed_values(df, column, allowed_values):
    """
    Check whether values belong to an allowed set.
    """

    return (
        df[column].notna()
        & ~df[column].isin(allowed_values)
    )


def validate_non_negative(df, column):
    """
    Check that numeric values are not negative.
    """

    return (
        df[column].notna()
        & (df[column] < 0)
    )