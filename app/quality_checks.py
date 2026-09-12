from app.quality_result import QualityResult
from app.validation_rules import (
    validate_allowed_values,
    validate_non_negative,
)


def _get_severity(rate):
    """
    Determine severity based on issue rate.
    """

    if rate == 0:
        return "info"
    elif rate <= 0.05:
        return "warning"
    elif rate <= 0.20:
        return "error"
    else:
        return "critical"


def _create_result(
    check_name,
    column,
    affected_count,
    total_count,
    message,
):
    """
    Create a standardized QualityResult.
    """

    rate = (
        affected_count / total_count
        if total_count > 0
        else 0
    )

    severity = _get_severity(rate)

    return QualityResult(
        check_name=check_name,
        column=column,
        affected_count=affected_count,
        total_count=total_count,
        rate=rate,
        severity=severity,
        message=message,
    )


def check_missing_values(df):
    """
    Check missing values in every column.
    """

    results = []
    total_rows = len(df)

    for column in df.columns:

        missing_count = int(
            df[column].isnull().sum()
        )

        if missing_count == 0:
            message = "No missing values detected."
        else:
            message = (
                f"{missing_count} missing value(s) detected."
            )

        results.append(
            _create_result(
                check_name="missing_values",
                column=column,
                affected_count=missing_count,
                total_count=total_rows,
                message=message,
            )
        )

    return results


def check_duplicates(df):
    """
    Check duplicate rows.
    """

    total_rows = len(df)

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count == 0:
        message = "No duplicate rows detected."
    else:
        message = (
            f"{duplicate_count} duplicate row(s) detected."
        )

    return _create_result(
        check_name="duplicates",
        column=None,
        affected_count=duplicate_count,
        total_count=total_rows,
        message=message,
    )


def _check_configured_invalid_values(
    df,
    validation_rules,
):
    """
    Internal function that applies configurable
    validation rules and returns one result per column.
    """

    results = []

    total_rows = len(df)

    if not validation_rules:
        return results

    for column, rules in validation_rules.items():

        if column not in df.columns:
            continue

        invalid_mask = None

        # ---------------------------------------------
        # Minimum value
        # ---------------------------------------------

        if "min" in rules:

            current_mask = (
                df[column].notna()
                & (df[column] < rules["min"])
            )

            invalid_mask = (
                current_mask
                if invalid_mask is None
                else invalid_mask | current_mask
            )

        # ---------------------------------------------
        # Maximum value
        # ---------------------------------------------

        if "max" in rules:

            current_mask = (
                df[column].notna()
                & (df[column] > rules["max"])
            )

            invalid_mask = (
                current_mask
                if invalid_mask is None
                else invalid_mask | current_mask
            )

        # ---------------------------------------------
        # Allowed values
        # ---------------------------------------------

        if "allowed_values" in rules:

            current_mask = validate_allowed_values(
                df,
                column,
                rules["allowed_values"],
            )

            invalid_mask = (
                current_mask
                if invalid_mask is None
                else invalid_mask | current_mask
            )

        # ---------------------------------------------
        # Non-negative
        # ---------------------------------------------

        if rules.get("non_negative", False):

            current_mask = validate_non_negative(
                df,
                column,
            )

            invalid_mask = (
                current_mask
                if invalid_mask is None
                else invalid_mask | current_mask
            )

        if invalid_mask is None:
            continue

        invalid_count = int(
            invalid_mask.sum()
        )

        message = (
            f"{invalid_count} invalid value(s) detected."
        )

        results.append(
            _create_result(
                check_name="invalid_values",
                column=column,
                affected_count=invalid_count,
                total_count=total_rows,
                message=message,
            )
        )

    return results


def check_invalid_values(
    df,
    validation_rules=None,
):
    """
    Check invalid values.

    Backward compatibility:
        When no validation_rules are supplied,
        this function checks the original age/salary
        rules and returns ONE QualityResult.

    New behavior:
        When validation_rules are supplied,
        configurable rules are applied to any columns
        and a list of QualityResult objects is returned.
    """

    total_rows = len(df)

    # =================================================
    # NEW GENERIC MODE
    # =================================================

    if validation_rules is not None:

        return _check_configured_invalid_values(
            df,
            validation_rules,
        )

    # =================================================
    # BACKWARD-COMPATIBLE MODE
    # =================================================

    invalid_count = 0

    # Age validation
    if "age" in df.columns:

        invalid_age = (
            df["age"].notna()
            & (
                (df["age"] < 0)
                | (df["age"] > 120)
            )
        )

        invalid_count += int(
            invalid_age.sum()
        )

    # Salary validation
    if "salary" in df.columns:

        invalid_salary = (
            df["salary"].notna()
            & (df["salary"] < 0)
        )

        invalid_count += int(
            invalid_salary.sum()
        )

    if invalid_count == 0:

        message = "No invalid values detected."

    else:

        message = (
            f"{invalid_count} invalid value(s) detected."
        )

    return _create_result(
        check_name="invalid_values",
        column=None,
        affected_count=invalid_count,
        total_count=total_rows,
        message=message,
    )


def check_outliers(df, column):
    """
    Detect statistical outliers using the IQR method.
    """

    total_rows = len(df)

    if total_rows == 0:

        return _create_result(
            check_name="outliers",
            column=column,
            affected_count=0,
            total_count=0,
            message="No data available.",
        )

    # Ignore missing values
    series = df[column].dropna()

    if len(series) < 4:

        return _create_result(
            check_name="outliers",
            column=column,
            affected_count=0,
            total_count=total_rows,
            message=(
                "Not enough data to reliably detect outliers."
            ),
        )

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    # If all values are identical
    if iqr == 0:

        outlier_count = 0

    else:

        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr

        outliers = (
            (df[column] < lower_limit)
            | (df[column] > upper_limit)
        )

        outlier_count = int(
            outliers.sum()
        )

    if outlier_count == 0:

        message = (
            "No statistical outliers detected."
        )

    else:

        message = (
            f"{outlier_count} statistical "
            f"outlier(s) detected."
        )

    return _create_result(
        check_name="outliers",
        column=column,
        affected_count=outlier_count,
        total_count=total_rows,
        message=message,
    )