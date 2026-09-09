def check_missing_values(df):
    """
    Check the number of missing values in each column.
    """

    missing_values = df.isnull().sum()

    return missing_values.to_dict()

def check_duplicates(df):
    """
    Check the number of duplicate rows in the dataset.
    """

    duplicate_count = df.duplicated().sum()

    return int(duplicate_count)

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