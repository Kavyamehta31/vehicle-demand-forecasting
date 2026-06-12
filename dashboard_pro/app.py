import streamlit as st
from pathlib import Path
from utils.metrics import kpi_card
from utils.data_loader import load_main_data
from utils.filters import create_filters
from utils.load_css import load_css

load_css()
st.markdown("""
<style>

/* Hide Streamlit menu */
#MainMenu {
    visibility: hidden;
}

/* Hide header */
header {
    visibility: hidden;
}

/* Hide footer */
footer {
    visibility: hidden;
}

/* Remove top spacing */
.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)
# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Vehicle Demand Forecasting Dashboard",
    page_icon="🚚",
    layout="wide"
)


# =====================================
# LOAD CSS
# =====================================

def load_css():

    css_file = Path(
        "dashboard_pro/assets/style.css"
    )

    if css_file.exists():

        with open(css_file) as f:

            st.markdown(
                f"""
                <style>
                {f.read()}
                </style>
                """,
                unsafe_allow_html=True
            )


load_css()


# =====================================
# LOAD DATA
# =====================================

df = load_main_data()


# =====================================
# SIDEBAR FILTERS
# =====================================

halb, engine, model, vehicle = create_filters(df)


# =====================================
# APPLY FILTERS
# =====================================

filtered_df = df.copy()

if halb != "All":
    filtered_df = filtered_df[
        filtered_df["Halb"].astype(str) == str(halb)
    ]

if engine != "All":
    filtered_df = filtered_df[
        filtered_df["engine_type"] == engine
    ]

if model != "All":
    filtered_df = filtered_df[
        filtered_df["map_model"] == model
    ]

if vehicle != "All":
    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"] == vehicle
    ]


# =====================================
# KPI CALCULATIONS
# =====================================

total_demand = int(
    filtered_df["demand"].sum()
)

unique_halbs = filtered_df["Halb"].nunique()

total_models = filtered_df["map_model"].nunique()

engine_types = filtered_df["engine_type"].nunique()


# =====================================
# HEADER
# =====================================

st.title(
    "🚚 Vehicle Demand Forecasting Dashboard"
)

st.markdown(
    """
    Analyze and forecast vehicle demand across different models,
    engines, HALBs and vehicle types using historical demand data.
    """
)

st.markdown("---")


# =====================================
# KPI SECTION
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    kpi_card(
        "Total Demand",
        f"{total_demand:,}"
    )

with col2:

    kpi_card(
        "Unique HALBs",
        unique_halbs
    )

with col3:

    kpi_card(
        "Total Models",
        total_models
    )

with col4:

    kpi_card(
        "Engine Types",
        engine_types
    )

st.markdown("---")


# =====================================
# DASHBOARD MODULES
# =====================================

st.subheader(
    "Dashboard Modules"
)

left_col, right_col = st.columns(2)

with left_col:

    st.info(
        """
📊 Executive Summary

📈 Data Overview

🔍 Exploratory Data Analysis (EDA)

🌳 Hierarchical Analysis
"""
    )

with right_col:

    st.info(
        """
🤖 Forecast Comparison

🏆 Model Performance

📉 Advanced Analytics

💡 Business Insights
"""
    )


# =====================================
# QUICK STATS
# =====================================

st.markdown("---")

st.subheader(
    "Project Overview"
)

col1, col2, col3 = st.columns(3)

with col1:

    kpi_card(
        "Forecast Horizon",
        "Jan-2025 → Mar-2025"
    )

with col2:

    kpi_card(
        "Forecast Models",
        "5"
    )

with col3:

    kpi_card(
        "Vehicle Types",
        filtered_df["Vehicle_Type"].nunique()
    )


# =====================================
# ABOUT PROJECT
# =====================================

st.markdown("---")

st.subheader(
    "About This Dashboard"
)

st.write(
    """
This dashboard provides an end-to-end analytics platform
for vehicle demand forecasting.

Features include:

• Executive KPI summaries

• Demand distribution analysis

• Exploratory Data Analysis (EDA)

• Hierarchical demand drill-down

• Forecast comparison across models

• Model performance benchmarking

• Advanced analytics and Pareto analysis

• Automated business insights generation
"""
)


# =====================================
# FOOTER
# =====================================

st.success(
    "Select a page from the sidebar to begin analysis."
)