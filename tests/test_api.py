"""
Tests for the FastAPI backend.
"""

from io import BytesIO

from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": (
            "Automated Data Quality API is running."
        )
    }


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_analyze_csv():

    with open(
        "data/sample_data.csv",
        "rb",
    ) as file:

        response = client.post(
            "/analyze",
            files={
                "file": (
                    "sample_data.csv",
                    file,
                    "text/csv",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == (
        "sample_data.csv"
    )

    assert "profile" in data

    assert "quality" in data

    assert "quality_score" in (
        data["quality"]
    )

    assert "quality_dimensions" in (
        data["quality"]
    )

    assert "metrics" in (
        data["quality"]
    )

    assert "column_types" in (
        data["quality"]
    )


def test_analyze_excel():

    excel_content = BytesIO()

    import pandas as pd

    test_df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": [
                "A",
                "B",
                "C",
            ],
            "price": [
                100,
                200,
                300,
            ],
        }
    )

    with pd.ExcelWriter(
        excel_content,
        engine="openpyxl",
    ) as writer:

        test_df.to_excel(
            writer,
            index=False,
        )

    excel_content.seek(0)

    response = client.post(
        "/analyze",
        files={
            "file": (
                "test_dataset.xlsx",
                excel_content,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == (
        "test_dataset.xlsx"
    )

    assert data["profile"]["rows"] == 3

    assert data["profile"]["columns"] == 3

    assert "quality" in data


def test_unsupported_file():

    response = client.post(
        "/analyze",
        files={
            "file": (
                "dataset.txt",
                b"some text",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    assert (
        "Unsupported file format"
        in response.json()["detail"]
    )


def test_empty_file():

    response = client.post(
        "/analyze",
        files={
            "file": (
                "empty.csv",
                b"",
                "text/csv",
            )
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Uploaded file is empty."
    )