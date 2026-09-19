"""
FastAPI application for the
Automated Data Quality & Data Observability Platform.
"""

from fastapi import FastAPI


app = FastAPI(
    title="Automated Data Quality API",
    description=(
        "Backend API for automated data quality "
        "analysis and observability."
    ),
    version="1.0.0",
)


@app.get("/")
def root():
    """
    Root endpoint.
    """

    return {
        "message": (
            "Automated Data Quality API is running."
        )
    }


@app.get("/health")
def health_check():
    """
    Health-check endpoint.
    """

    return {
        "status": "healthy"
    }