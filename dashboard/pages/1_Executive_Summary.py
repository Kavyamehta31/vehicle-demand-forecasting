import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Executive Summary",
    layout="wide"
)

st.title("📊 Executive Summary")
comparison_df = pd.read_excel(
    "outputs/master_model_comparison.xlsx"
)
# ==================================
# KPI CARDS
# ==================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Series",
        "2070"
    )

with col2:
    st.metric(
        "Active Series",
        "472"
    )

with col3:
    st.metric(
        "Intermittent Series",
        "1598"
    )

best_model = (
    comparison_df
    .sort_values(
        by="Average_Accuracy",
        ascending=False
    )
    .iloc[0]
)

with col4:

    st.metric(
        "Best Model",
        best_model["Model"]
    )
with col5:

    st.metric(
        "Best Accuracy",
        f"{best_model['Average_Accuracy']:.2f}%"
    )

st.markdown("---")

# ==================================
# MODEL PERFORMANCE
# ==================================



st.subheader("Model Leaderboard")

leaderboard = (
    comparison_df[
        [
            "Model",
            "Average_MAE",
            "Average_Accuracy"
        ]
    ]
    .sort_values(
        by="Average_Accuracy",
        ascending=False
    )
    .reset_index(drop=True)
)

leaderboard.index += 1

leaderboard.index.name = "Rank"

st.dataframe(
    leaderboard,
    use_container_width=True
)

# ==================================
# CHARTS
# ==================================

col1, col2 = st.columns(2)

with col1:

    pie_df = pd.DataFrame(
        {
            "Category": [
                "Active",
                "Intermittent"
            ],
            "Count": [
                472,
                1598
            ]
        }
    )

    fig = px.pie(
        pie_df,
        names="Category",
        values="Count",
        title="Series Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig2 = px.bar(
        comparison_df,
        x="Model",
        y="Average_Accuracy",
        text="Average_Accuracy",
        title="Model Accuracy Comparison"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.markdown("---")

st.subheader("Project Summary")

st.write(
    """
    • Total Forecasting Series: 2070

    • Active Series: 472

    • Intermittent Series: 1598

    • Forecast Horizon: Jan-2025 to Mar-2025

    • Implemented Models:
      Moving Average, SES, Holt, ARIMA,
      Recursive Linear Regression

    • Dashboard enables vehicle-level
      forecast exploration and model comparison.
    """
)