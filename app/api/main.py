"""
FastAPI application for the
Automated Data Quality & Data Observability Platform.
"""

import os
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.analyzer import analyze_dataset


app = FastAPI(
    title="Automated Data Quality API",
    description=(
        "Backend API for automated data quality "
        "analysis and observability."
    ),
    version="1.0.0",
)


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
}


def quality_result_to_dict(result):
    """
    Convert a QualityResult object into
    a JSON-serializable dictionary.
    """

    return {
        "check_name": result.check_name,
        "column": result.column,
        "affected_count": result.affected_count,
        "total_count": result.total_count,
        "rate": result.rate,
        "severity": result.severity,
        "message": result.message,
        "passed": result.passed,
    }


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


@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
):
    """
    Analyze an uploaded CSV or Excel dataset.
    """

    # --------------------------------------------------
    # Validate filename
    # --------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename was provided.",
        )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format. "
                "Supported formats: CSV, XLSX, XLS."
            ),
        )

    temp_file_path = None

    try:

        # --------------------------------------------------
        # Read uploaded file
        # --------------------------------------------------

        file_content = await file.read()

        if not file_content:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        # --------------------------------------------------
        # Save temporary file
        # --------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:

            temp_file.write(
                file_content
            )

            temp_file_path = temp_file.name

        # --------------------------------------------------
        # Run existing analysis engine
        # --------------------------------------------------

        analysis = analyze_dataset(
            temp_file_path
        )

        profile = analysis[
            "profile"
        ]

        quality = analysis[
            "quality"
        ]

        # --------------------------------------------------
        # Convert QualityResult objects
        # --------------------------------------------------

        missing_results = [
            quality_result_to_dict(result)
            for result in quality[
                "missing_results"
            ]
        ]

        invalid_results = [
            quality_result_to_dict(result)
            for result in quality[
                "invalid_results"
            ]
        ]

        outlier_results = [
            quality_result_to_dict(result)
            for result in quality[
                "outlier_results"
            ]
        ]

        duplicate_result = (
            quality_result_to_dict(
                quality[
                    "duplicate_result"
                ]
            )
        )

        # --------------------------------------------------
        # Build API response
        # --------------------------------------------------

        return {
            "filename": file.filename,

            "profile": {
                "rows": profile[
                    "rows"
                ],

                "columns": profile[
                    "columns"
                ],

                "column_names": profile[
                    "column_names"
                ],

                "data_types": profile[
                    "data_types"
                ],
            },

            "quality": {
                "quality_score": quality[
                    "quality_score"
                ],

                "quality_dimensions": quality[
                    "quality_dimensions"
                ],

                "metrics": quality[
                    "metrics"
                ],

                "column_types": quality[
                    "column_types"
                ],

                "missing_results": missing_results,

                "duplicate_result": duplicate_result,

                "invalid_results": invalid_results,

                "outlier_results": outlier_results,
            },
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Dataset analysis failed: {e}"
            ),
        )

    finally:

        # --------------------------------------------------
        # Delete temporary file
        # --------------------------------------------------

        if temp_file_path is not None:

            try:

                os.remove(
                    temp_file_path
                )

            except OSError:

                pass