import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from utils.data_loader import load_main_data
from utils.filters import create_filters
from utils.metrics import kpi_card
from utils.theme import load_css

load_css()

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📊",
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

comparison_df = pd.read_excel(
    "outputs/master_model_comparison.xlsx"
)


# =====================================
# FILTERS
# =====================================

halb, engine, model, vehicle = create_filters(df)

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
# KPI VALUES
# =====================================

total_demand = int(
    filtered_df["demand"].sum()
)

unique_halbs = filtered_df["Halb"].nunique()

total_models = filtered_df["map_model"].nunique()

engine_types = filtered_df["engine_type"].nunique()


# =====================================
# PAGE TITLE
# =====================================

st.title("📊 Executive Summary")

st.markdown(
    """
    High-level overview of vehicle demand,
    forecasting coverage and model performance.
    """
)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================
# KPI CARDS
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


# =====================================
# EXECUTIVE HIGHLIGHTS
# =====================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Executive Highlights")

left_col, right_col = st.columns(2)

with left_col:

    st.info(
        f"""
🚚 Total Demand Analyzed: {total_demand:,}

🏭 Unique HALBs: {unique_halbs}

📦 Total Models: {total_models}

⚙️ Engine Types: {engine_types}
"""
    )

with right_col:

    st.success(
        """
✔ Demand forecasting system loaded successfully

✔ Filters applied dynamically

✔ Dashboard ready for detailed analysis

✔ Navigate using sidebar pages
"""
    )


# =====================================
# SUMMARY TABLE
# =====================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Summary Metrics")

overview_df = pd.DataFrame(
    {
        "Metric": [
            "Total Demand",
            "Unique HALBs",
            "Total Models",
            "Engine Types"
        ],
        "Value": [
            f"{total_demand:,}",
            unique_halbs,
            total_models,
            engine_types
        ]
    }
)

st.dataframe(
    overview_df,
    use_container_width=True
)


# =====================================
# MODEL LEADERBOARD
# =====================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🏆 Model Leaderboard")

try:

    leaderboard = comparison_df.sort_values(
        by="Average_Accuracy",
        ascending=False
    )

    st.dataframe(
        leaderboard,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"Leaderboard could not be loaded: {e}"
    )


# =====================================
# ACCURACY COMPARISON
# =====================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📈 Forecast Accuracy Comparison")

try:

    fig = px.bar(
        comparison_df,
        x="Model",
        y="Average_Accuracy",
        text="Average_Accuracy",
        color="Average_Accuracy"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"Accuracy chart error: {e}"
    )


# =====================================
# MAE COMPARISON
# =====================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📉 MAE Comparison")

try:

    fig2 = px.bar(
        comparison_df,
        x="Model",
        y="Average_MAE",
        text="Average_MAE",
        color="Average_MAE"
    )

    fig2.update_layout(
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"MAE chart error: {e}"
    )


# =====================================
# BEST MODEL
# =====================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🥇 Best Performing Model")

try:

    best_model = comparison_df.sort_values(
        by="Average_Accuracy",
        ascending=False
    ).iloc[0]

    st.success(
        f"""
Best Model: {best_model['Model']}

Average Accuracy: {best_model['Average_Accuracy']:.2f}%

Average MAE: {best_model['Average_MAE']:.2f}
"""
    )

except Exception as e:

    st.warning(
        f"Best model calculation error: {e}"
    )