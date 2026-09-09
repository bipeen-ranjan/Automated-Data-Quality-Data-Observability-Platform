from app.quality_result import QualityResult


def check_missing_values(df):
    """
    Check missing values in each column.
    Returns one QualityResult for each column.
    """

    results = []
    total_rows = len(df)

    for column in df.columns:
        missing_count = int(df[column].isnull().sum())

        rate = missing_count / total_rows if total_rows > 0 else 0

        if missing_count == 0:
            severity = "info"
            message = "No missing values detected."
        elif rate <= 0.05:
            severity = "warning"
            message = "A small number of missing values detected."
        elif rate <= 0.20:
            severity = "error"
            message = "A significant number of missing values detected."
        else:
            severity = "critical"
            message = "A large number of missing values detected."

        results.append(
            QualityResult(
                check_name="missing_values",
                column=column,
                affected_count=missing_count,
                total_count=total_rows,
                rate=rate,
                severity=severity,
                message=message,
            )
        )

    return results



def check_duplicates(df):
    """
    Check for duplicate rows in the dataset.

    Returns a QualityResult describing the duplicate rows.
    """

    total_rows = len(df)

    duplicate_count = int(df.duplicated().sum())

    rate = duplicate_count / total_rows if total_rows > 0 else 0

    if duplicate_count == 0:
        severity = "info"
        message = "No duplicate rows detected."
    elif rate <= 0.05:
        severity = "warning"
        message = "A small number of duplicate rows detected."
    elif rate <= 0.20:
        severity = "error"
        message = "A significant number of duplicate rows detected."
    else:
        severity = "critical"
        message = "A large number of duplicate rows detected."

    return QualityResult(
        check_name="duplicates",
        column=None,
        affected_count=duplicate_count,
        total_count=total_rows,
        rate=rate,
        severity=severity,
        message=message,
    )

def check_invalid_values(df):
    """
    Check for invalid age and salary values.
    """

    invalid_age = (df["age"] < 0) | (df["age"] > 120)
    invalid_salary = df["salary"] < 0

    invalid_count = invalid_age.sum() + invalid_salary.sum()

    return int(invalid_count)


def check_outliers(df, column):
    """
    Detect outliers in a numerical column using the IQR method.
    """

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    outliers = df[
        (df[column] < lower_limit) |
        (df[column] > upper_limit)
    ]

    return len(outliers)