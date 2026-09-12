import pandas as pd

from app.column_classifier import classify_dataframe


def test_classify_dataframe():

    df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "age": [20, 30, 40, 50],
            "rating": [1, 2, 3, 4],
            "name": [
                "A",
                "B",
                "C",
                "D",
            ],
            "order_date": [
                "2025-01-01",
                "2025-01-02",
                "2025-01-03",
                "2025-01-04",
            ],
        }
    )

    result = classify_dataframe(df)

    assert result["customer_id"] == "identifier"
    assert result["age"] == "numeric"
    assert result["rating"] == "categorical"
    assert result["name"] == "categorical"
    assert result["order_date"] == "datetime"