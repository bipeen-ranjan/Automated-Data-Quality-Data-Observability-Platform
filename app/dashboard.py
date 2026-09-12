import os
import tempfile

import pandas as pd
import plotly.express as px
import streamlit as st

from app.analyzer import analyze_dataset


st.set_page_config(
    page_title="Data Quality & Observability",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #777;
        margin-bottom: 1.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📊 Data Quality")

    st.markdown(
        """
        ### Automated Data Quality Platform

        Upload a dataset and automatically analyze:

        - Missing values
        - Duplicate rows
        - Invalid values
        - Statistical outliers
        - Dataset profile
        - Column types
        - Quality dimensions
        - Overall quality score
        """
    )

    st.divider()

    st.markdown("### Supported Files")

    st.markdown(
        """
        Currently supported:

        - CSV
        - Excel
        """
    )

    st.divider()

    st.markdown("### Automatic Analysis")

    st.markdown(
        """
        The system automatically identifies:

        - Identifier columns
        - Numeric columns
        - Categorical columns
        - Date/time columns
        - Text columns
        """
    )

    st.divider()

    st.markdown("### Quality Score")

    st.markdown(
        """
        The overall score combines:

        - Completeness — 40%
        - Uniqueness — 20%
        - Validity — 25%
        - Consistency — 15%
        """
    )

    st.divider()

    st.caption(
        "Automated Data Quality & Data Observability Platform"
    )


# ==========================================================
# PAGE HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">Automated Data Quality Platform</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
    Upload a dataset and automatically evaluate its quality.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# FILE UPLOAD
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx", "xls"],
    help="Upload a CSV or Excel dataset.",
)


# ==========================================================
# LANDING PAGE
# ==========================================================

if uploaded_file is None:

    st.info(
        "👆 Upload a CSV or Excel file above to begin."
    )

    st.markdown("### How It Works")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown("### 1️⃣ Upload")

        st.write(
            "Upload any supported tabular dataset."
        )

    with col2:

        st.markdown("### 2️⃣ Profile")

        st.write(
            "The system examines the structure and contents."
        )

    with col3:

        st.markdown("### 3️⃣ Analyze")

        st.write(
            "Automated quality checks identify potential issues."
        )

    with col4:

        st.markdown("### 4️⃣ Score")

        st.write(
            "A weighted score summarizes the dataset condition."
        )

    st.stop()


# ==========================================================
# PREVIEW FILE
# ==========================================================

try:

    file_name_lower = uploaded_file.name.lower()

    if file_name_lower.endswith(".csv"):

        preview_df = pd.read_csv(
            uploaded_file
        )

    elif (
        file_name_lower.endswith(".xlsx")
        or file_name_lower.endswith(".xls")
    ):

        preview_df = pd.read_excel(
            uploaded_file
        )

    else:

        st.error(
            "Unsupported file format."
        )

        st.stop()

except Exception as e:

    st.error(
        f"Unable to read the uploaded file: {e}"
    )

    st.stop()


# ==========================================================
# DATASET INFORMATION
# ==========================================================

st.markdown("### Dataset Information")

info_col1, info_col2, info_col3, info_col4 = st.columns(4)

with info_col1:

    st.metric(
        "File Name",
        uploaded_file.name,
    )

with info_col2:

    st.metric(
        "Rows",
        f"{len(preview_df):,}",
    )

with info_col3:

    st.metric(
        "Columns",
        len(preview_df.columns),
    )

with info_col4:

    st.metric(
        "File Size",
        f"{uploaded_file.size / 1024:.1f} KB",
    )


# ==========================================================
# DATASET PREVIEW
# ==========================================================

st.markdown("### Dataset Preview")

st.dataframe(
    preview_df.head(10),
    use_container_width=True,
)


# ==========================================================
# BASIC COLUMN INFORMATION
# ==========================================================

with st.expander(
    "🔎 View Basic Column Information"
):

    column_info = pd.DataFrame(
        {
            "Column": preview_df.columns,

            "Pandas Data Type": [
                str(
                    preview_df[column].dtype
                )
                for column in preview_df.columns
            ],

            "Missing Values": [
                int(
                    preview_df[column]
                    .isnull()
                    .sum()
                )
                for column in preview_df.columns
            ],

            "Unique Values": [
                int(
                    preview_df[column]
                    .nunique()
                )
                for column in preview_df.columns
            ],
        }
    )

    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True,
    )


# ==========================================================
# RUN ANALYSIS
# ==========================================================

st.markdown("### Run Analysis")

analyze_button = st.button(
    "🔍 Analyze Dataset",
    type="primary",
    use_container_width=True,
)


if analyze_button:

    temp_file_path = None

    try:

        # --------------------------------------------------
        # Save uploaded file temporarily
        # --------------------------------------------------

        suffix = os.path.splitext(
            uploaded_file.name
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_file_path = temp_file.name

        # --------------------------------------------------
        # Analyze
        # --------------------------------------------------

        with st.spinner(
            "Analyzing dataset..."
        ):

            analysis = analyze_dataset(
                temp_file_path
            )

        profile = analysis["profile"]

        quality = analysis["quality"]

        missing_results = quality[
            "missing_results"
        ]

        duplicate_result = quality[
            "duplicate_result"
        ]

        invalid_results = quality[
            "invalid_results"
        ]

        outlier_results = quality[
            "outlier_results"
        ]

        column_types = quality[
            "column_types"
        ]

        quality_score = quality[
            "quality_score"
        ]

        quality_dimensions = quality[
            "quality_dimensions"
        ]

        metrics = quality[
            "metrics"
        ]

        # --------------------------------------------------
        # Issue counts
        # --------------------------------------------------

        missing_count = metrics[
            "missing_count"
        ]

        duplicate_count = metrics[
            "duplicate_count"
        ]

        invalid_count = metrics[
            "invalid_count"
        ]

        outlier_count = metrics[
            "outlier_count"
        ]

        total_cells = metrics[
            "total_cells"
        ]

        numeric_observations = metrics[
            "numeric_observations"
        ]

        missing_rate = metrics[
            "missing_rate"
        ]

        duplicate_rate = metrics[
            "duplicate_rate"
        ]

        invalid_rate = metrics[
            "invalid_rate"
        ]

        outlier_rate = metrics[
            "outlier_rate"
        ]

        # --------------------------------------------------
        # Rows containing missing values
        # --------------------------------------------------

        rows_with_missing = int(
            preview_df
            .isnull()
            .any(axis=1)
            .sum()
        )

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        if quality_score >= 90:

            status = "Excellent"
            status_icon = "🟢"

        elif quality_score >= 75:

            status = "Good"
            status_icon = "🟡"

        elif quality_score >= 50:

            status = "Needs Improvement"
            status_icon = "🟠"

        else:

            status = "Poor"
            status_icon = "🔴"

        # --------------------------------------------------
        # Success message
        # --------------------------------------------------

        st.success(
            "Dataset analysis completed successfully."
        )

        st.markdown("---")

        # ==================================================
        # QUALITY OVERVIEW
        # ==================================================

        st.markdown(
            "## 📊 Quality Overview"
        )

        score_col, status_col, rows_col, columns_col = st.columns(
            4
        )

        with score_col:

            st.metric(
                "Quality Score",
                f"{quality_score:.2f}/100",
            )

        with status_col:

            st.metric(
                "Status",
                f"{status_icon} {status}",
            )

        with rows_col:

            st.metric(
                "Rows",
                f"{profile['rows']:,}",
            )

        with columns_col:

            st.metric(
                "Columns",
                profile["columns"],
            )

        # ==================================================
        # QUALITY DIMENSIONS
        # ==================================================

        st.markdown(
            "### 🎯 Quality Dimensions"
        )

        st.caption(
            "The overall score is calculated from four "
            "independent data-quality dimensions."
        )

        dimension_col1, dimension_col2, dimension_col3, dimension_col4 = st.columns(
            4
        )

        with dimension_col1:

            st.metric(
                "Completeness",
                f"{quality_dimensions['completeness']:.2f}/100",
                "40% weight",
            )

        with dimension_col2:

            st.metric(
                "Uniqueness",
                f"{quality_dimensions['uniqueness']:.2f}/100",
                "20% weight",
            )

        with dimension_col3:

            st.metric(
                "Validity",
                f"{quality_dimensions['validity']:.2f}/100",
                "25% weight",
            )

        with dimension_col4:

            st.metric(
                "Consistency",
                f"{quality_dimensions['consistency']:.2f}/100",
                "15% weight",
            )

        # --------------------------------------------------
        # Dimension chart
        # --------------------------------------------------

        dimension_df = pd.DataFrame(
            {
                "Dimension": [
                    "Completeness",
                    "Uniqueness",
                    "Validity",
                    "Consistency",
                ],

                "Score": [
                    quality_dimensions[
                        "completeness"
                    ],

                    quality_dimensions[
                        "uniqueness"
                    ],

                    quality_dimensions[
                        "validity"
                    ],

                    quality_dimensions[
                        "consistency"
                    ],
                ],
            }
        )

        fig_dimensions = px.bar(
            dimension_df,
            x="Dimension",
            y="Score",
            range_y=[0, 100],
            title="Quality Dimension Scores",
            text="Score",
        )

        fig_dimensions.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
        )

        fig_dimensions.update_layout(
            xaxis_title="Quality Dimension",
            yaxis_title="Score",
        )

        st.plotly_chart(
            fig_dimensions,
            use_container_width=True,
        )

        # ==================================================
        # ISSUE SUMMARY
        # ==================================================

        st.markdown(
            "### Issue Summary"
        )

        issue_col1, issue_col2, issue_col3, issue_col4 = st.columns(
            4
        )

        with issue_col1:

            st.metric(
                "Missing Cells",
                f"{missing_count:,}",
            )

        with issue_col2:

            st.metric(
                "Duplicate Rows",
                f"{duplicate_count:,}",
            )

        with issue_col3:

            st.metric(
                "Invalid Values",
                f"{invalid_count:,}",
            )

        with issue_col4:

            st.metric(
                "Statistical Outliers",
                f"{outlier_count:,}",
            )

        # ==================================================
        # DATA QUALITY DETAILS
        # ==================================================

        st.markdown(
            "### 📌 Data Quality Details"
        )

        detail_col1, detail_col2, detail_col3 = st.columns(
            3
        )

        with detail_col1:

            st.metric(
                "Rows With Missing Data",
                f"{rows_with_missing:,}",
            )

        with detail_col2:

            numeric_count = sum(
                1
                for value in column_types.values()
                if value == "numeric"
            )

            st.metric(
                "Numeric Columns",
                numeric_count,
            )

        with detail_col3:

            categorical_count = sum(
                1
                for value in column_types.values()
                if value == "categorical"
            )

            st.metric(
                "Categorical Columns",
                categorical_count,
            )

        # ==================================================
        # QUALITY METRICS
        # ==================================================

        st.markdown(
            "### 📐 Quality Metrics"
        )

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(
            4
        )

        with metric_col1:

            st.metric(
                "Total Cells",
                f"{total_cells:,}",
            )

        with metric_col2:

            st.metric(
                "Missing Rate",
                f"{missing_rate * 100:.2f}%",
            )

        with metric_col3:

            st.metric(
                "Duplicate Rate",
                f"{duplicate_rate * 100:.2f}%",
            )

        with metric_col4:

            st.metric(
                "Invalid Rate",
                f"{invalid_rate * 100:.2f}%",
            )

        metric_col5, metric_col6 = st.columns(2)

        with metric_col5:

            st.metric(
                "Numeric Observations",
                f"{numeric_observations:,}",
            )

        with metric_col6:

            st.metric(
                "Outlier Rate",
                f"{outlier_rate * 100:.2f}%",
            )

        # ==================================================
        # TABS
        # ==================================================

        (
            tab_overview,
            tab_classification,
            tab_missing,
            tab_duplicates,
            tab_invalid,
            tab_outliers,
        ) = st.tabs(
            [
                "📈 Overview",
                "🔎 Column Classification",
                "⚠️ Missing Values",
                "📋 Duplicates",
                "❌ Invalid Values",
                "📊 Outliers",
            ]
        )

        # ==================================================
        # OVERVIEW TAB
        # ==================================================

        with tab_overview:

            st.markdown(
                "### Dataset Profile"
            )

            profile_col1, profile_col2 = st.columns(
                2
            )

            with profile_col1:

                st.write(
                    "**Rows:**",
                    profile["rows"],
                )

                st.write(
                    "**Columns:**",
                    profile["columns"],
                )

                st.write(
                    "**Column Names:**"
                )

                st.write(
                    ", ".join(
                        profile["column_names"]
                    )
                )

            with profile_col2:

                st.write(
                    "**Pandas Data Types**"
                )

                dtype_df = pd.DataFrame(
                    {
                        "Column": list(
                            profile[
                                "data_types"
                            ].keys()
                        ),

                        "Data Type": list(
                            profile[
                                "data_types"
                            ].values()
                        ),
                    }
                )

                st.dataframe(
                    dtype_df,
                    use_container_width=True,
                    hide_index=True,
                )

            st.markdown(
                "### Issue Distribution"
            )

            issue_data = pd.DataFrame(
                {
                    "Issue Type": [
                        "Missing Values",
                        "Duplicates",
                        "Invalid Values",
                        "Outliers",
                    ],

                    "Count": [
                        missing_count,
                        duplicate_count,
                        invalid_count,
                        outlier_count,
                    ],
                }
            )

            fig = px.bar(
                issue_data,
                x="Issue Type",
                y="Count",
                title="Data Quality Issues",
            )

            fig.update_layout(
                xaxis_title="Issue Type",
                yaxis_title="Number of Issues",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        # ==================================================
        # CLASSIFICATION TAB
        # ==================================================

        with tab_classification:

            st.markdown(
                "### 🔎 Automatic Column Classification"
            )

            st.write(
                """
                The platform automatically classifies each
                column before deciding which statistical
                quality checks are appropriate.
                """
            )

            classification_data = []

            for column in profile["column_names"]:

                classification_data.append(
                    {
                        "Column": column,

                        "Pandas Type": profile[
                            "data_types"
                        ][column],

                        "Detected Type": column_types[
                            column
                        ],

                        "Missing Values": int(
                            preview_df[
                                column
                            ].isnull().sum()
                        ),

                        "Unique Values": int(
                            preview_df[
                                column
                            ].nunique()
                        ),
                    }
                )

            classification_df = pd.DataFrame(
                classification_data
            )

            st.dataframe(
                classification_df,
                use_container_width=True,
                hide_index=True,
            )

            st.markdown(
                "### Classification Meaning"
            )

            explanation_col1, explanation_col2 = st.columns(
                2
            )

            with explanation_col1:

                st.markdown(
                    """
                    **Identifier**

                    Values primarily used to identify
                    individual records.

                    Example:
                    `customer_id`, `PassengerId`

                    **Numeric**

                    Continuous numerical measurements
                    suitable for statistical analysis.

                    Example:
                    `age`, `price`, `salary`
                    """
                )

            with explanation_col2:

                st.markdown(
                    """
                    **Categorical**

                    Values representing categories or
                    low-cardinality groups.

                    Example:
                    `gender`, `department`, `Pclass`

                    **Datetime**

                    Columns containing dates or timestamps.

                    Example:
                    `order_date`, `start_date`
                    """
                )

        # ==================================================
        # MISSING TAB
        # ==================================================

        with tab_missing:

            st.markdown(
                "### Missing Value Analysis"
            )

            missing_data = []

            for result in missing_results:

                missing_data.append(
                    {
                        "Column": result.column,

                        "Missing Count": (
                            result.affected_count
                        ),

                        "Missing Rate": (
                            f"{result.rate * 100:.2f}%"
                        ),

                        "Severity": (
                            result.severity
                        ),

                        "Status": (
                            "PASS"
                            if result.passed
                            else "ISSUE"
                        ),

                        "Message": result.message,
                    }
                )

            missing_df = pd.DataFrame(
                missing_data
            )

            st.dataframe(
                missing_df,
                use_container_width=True,
                hide_index=True,
            )

            if missing_count > 0:

                chart_df = pd.DataFrame(
                    {
                        "Column": [
                            result.column
                            for result in missing_results
                            if result.affected_count > 0
                        ],

                        "Missing Values": [
                            result.affected_count
                            for result in missing_results
                            if result.affected_count > 0
                        ],
                    }
                )

                if not chart_df.empty:

                    fig = px.bar(
                        chart_df,
                        x="Column",
                        y="Missing Values",
                        title="Missing Values by Column",
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                    )

            else:

                st.success(
                    "No missing values detected."
                )

        # ==================================================
        # DUPLICATES TAB
        # ==================================================

        with tab_duplicates:

            st.markdown(
                "### Duplicate Row Analysis"
            )

            duplicate_data = pd.DataFrame(
                [
                    {
                        "Check": "Duplicate Rows",

                        "Affected Rows": (
                            duplicate_result.affected_count
                        ),

                        "Rate": (
                            f"{duplicate_result.rate * 100:.2f}%"
                        ),

                        "Severity": (
                            duplicate_result.severity
                        ),

                        "Status": (
                            "PASS"
                            if duplicate_result.passed
                            else "ISSUE"
                        ),

                        "Message": (
                            duplicate_result.message
                        ),
                    }
                ]
            )

            st.dataframe(
                duplicate_data,
                use_container_width=True,
                hide_index=True,
            )

            if duplicate_count == 0:

                st.success(
                    "No duplicate rows detected."
                )

            else:

                st.warning(
                    f"{duplicate_count:,} duplicate "
                    "row(s) detected."
                )

        # ==================================================
        # INVALID TAB
        # ==================================================

        with tab_invalid:

            st.markdown(
                "### Invalid Value Analysis"
            )

            if not invalid_results:

                st.info(
                    "No configurable validation rules "
                    "were applied to this dataset."
                )

                st.markdown(
                    """
                    The validation engine supports
                    configurable rules such as:

                    - Minimum values
                    - Maximum values
                    - Non-negative values
                    - Allowed categorical values

                    Rules can be configured for any
                    dataset-specific column.
                    """
                )

            else:

                invalid_data = []

                for result in invalid_results:

                    invalid_data.append(
                        {
                            "Column": result.column,

                            "Invalid Count": (
                                result.affected_count
                            ),

                            "Invalid Rate": (
                                f"{result.rate * 100:.2f}%"
                            ),

                            "Severity": (
                                result.severity
                            ),

                            "Status": (
                                "PASS"
                                if result.passed
                                else "ISSUE"
                            ),

                            "Message": result.message,
                        }
                    )

                invalid_df = pd.DataFrame(
                    invalid_data
                )

                st.dataframe(
                    invalid_df,
                    use_container_width=True,
                    hide_index=True,
                )

                if invalid_count == 0:

                    st.success(
                        "No invalid values detected."
                    )

        # ==================================================
        # OUTLIER TAB
        # ==================================================

        with tab_outliers:

            st.markdown(
                "### Statistical Outlier Analysis"
            )

            st.info(
                """
                Statistical outliers are potential unusual
                observations identified using the IQR method.
                They are not automatically considered invalid data.
                """
            )

            if not outlier_results:

                st.info(
                    "No continuous numeric columns were "
                    "identified for IQR outlier analysis."
                )

            else:

                outlier_data = []

                for result in outlier_results:

                    outlier_data.append(
                        {
                            "Column": result.column,

                            "Outlier Count": (
                                result.affected_count
                            ),

                            "Outlier Rate": (
                                f"{result.rate * 100:.2f}%"
                            ),

                            "Severity": (
                                result.severity
                            ),

                            "Status": (
                                "PASS"
                                if result.passed
                                else "ISSUE"
                            ),

                            "Message": result.message,
                        }
                    )

                outlier_df = pd.DataFrame(
                    outlier_data
                )

                st.dataframe(
                    outlier_df,
                    use_container_width=True,
                    hide_index=True,
                )

                columns_with_outliers = [
                    result
                    for result in outlier_results
                    if result.affected_count > 0
                ]

                if columns_with_outliers:

                    chart_df = pd.DataFrame(
                        {
                            "Column": [
                                result.column
                                for result in columns_with_outliers
                            ],

                            "Outliers": [
                                result.affected_count
                                for result in columns_with_outliers
                            ],
                        }
                    )

                    fig = px.bar(
                        chart_df,
                        x="Column",
                        y="Outliers",
                        title=(
                            "Statistical Outliers "
                            "by Numeric Column"
                        ),
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                    )

                else:

                    st.success(
                        "No statistical outliers detected."
                    )

        # ==================================================
        # DETAILED RESULTS
        # ==================================================

        with st.expander(
            "🔧 View Detailed Analysis Results"
        ):

            st.markdown(
                "### Quality Dimensions"
            )

            st.write(
                quality_dimensions
            )

            st.markdown(
                "### Quality Metrics"
            )

            st.write(
                metrics
            )

            st.markdown(
                "### Column Classification"
            )

            st.write(
                column_types
            )

            st.markdown(
                "### Missing Value Results"
            )

            st.write(
                [
                    {
                        "column": result.column,
                        "affected": result.affected_count,
                        "rate": result.rate,
                        "severity": result.severity,
                    }
                    for result in missing_results
                ]
            )

            st.markdown(
                "### Duplicate Result"
            )

            st.write(
                {
                    "affected": (
                        duplicate_result.affected_count
                    ),
                    "rate": (
                        duplicate_result.rate
                    ),
                    "severity": (
                        duplicate_result.severity
                    ),
                }
            )

            st.markdown(
                "### Invalid Value Results"
            )

            st.write(
                [
                    {
                        "column": result.column,
                        "affected": result.affected_count,
                        "rate": result.rate,
                        "severity": result.severity,
                    }
                    for result in invalid_results
                ]
            )

            st.markdown(
                "### Outlier Results"
            )

            st.write(
                [
                    {
                        "column": result.column,
                        "affected": result.affected_count,
                        "rate": result.rate,
                        "severity": result.severity,
                    }
                    for result in outlier_results
                ]
            )

    except Exception as e:

        st.error(
            f"An error occurred during analysis: {e}"
        )

    finally:

        if temp_file_path is not None:

            try:

                os.remove(
                    temp_file_path
                )

            except OSError:

                pass