import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from utils.data_loader import load_main_data
from utils.filters import create_filters


# =====================================================
# PAGE TITLE
# =====================================================

st.title("📊 Model Performance")


# =====================================================
# LOAD DATA
# =====================================================

df = load_main_data()

arima = pd.read_excel(
    "outputs/arima_results.xlsx"
)

holt = pd.read_excel(
    "outputs/holt_results.xlsx"
)

moving = pd.read_excel(
    "outputs/moving_average_results.xlsx"
)

ses = pd.read_excel(
    "outputs/ses_results.xlsx"
)


# =====================================================
# ADD MODEL NAME
# =====================================================

arima["Model Used"] = "ARIMA"
holt["Model Used"] = "Holt"
moving["Model Used"] = "Moving Average"
ses["Model Used"] = "SES"


# =====================================================
# COMBINE ALL MODELS
# =====================================================

performance_df = pd.concat(
    [
        arima,
        holt,
        moving,
        ses
    ],
    ignore_index=True
)


# =====================================================
# FILTERS
# =====================================================

halb, engine, model, vehicle = create_filters(df)

if halb != "All":
    performance_df = performance_df[
        performance_df["Halb"].astype(str) == str(halb)
    ]

if engine != "All":
    performance_df = performance_df[
        performance_df["engine_type"] == engine
    ]

if model != "All":
    performance_df = performance_df[
        performance_df["map_model"] == model
    ]

if vehicle != "All":
    performance_df = performance_df[
        performance_df["Vehicle_Type"] == vehicle
    ]


# =====================================================
# LEADERBOARD
# =====================================================

leaderboard = (
    performance_df
    .groupby("Model Used")
    .agg(
        {
            "Accuracy": "mean",
            "MAPE": "mean",
            "MAE": "mean"
        }
    )
    .reset_index()
)

leaderboard = leaderboard.sort_values(
    "Accuracy",
    ascending=False
)


# =====================================================
# KPI CARDS
# =====================================================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Forecast Models",
        leaderboard.shape[0]
    )

with col2:
    st.metric(
        "HALBs",
        performance_df["Halb"].nunique()
    )

with col3:
    st.metric(
        "Avg Accuracy",
        f"{leaderboard['Accuracy'].mean():.2f}%"
    )

with col4:
    st.metric(
        "Best Accuracy",
        f"{leaderboard['Accuracy'].max():.2f}%"
    )


# =====================================================
# ROW 1
# =====================================================

st.markdown("---")

col5, col6 = st.columns([1, 1])

with col5:

    st.subheader(
        "Accuracy Leaderboard"
    )

    leaderboard_display = leaderboard.copy()

    leaderboard_display["Accuracy"] = (
        leaderboard_display["Accuracy"]
        .round(2)
    )

    leaderboard_display["MAPE"] = (
        leaderboard_display["MAPE"]
        .round(2)
    )

    leaderboard_display["MAE"] = (
        leaderboard_display["MAE"]
        .round(2)
    )

    st.dataframe(
        leaderboard_display,
        use_container_width=True
    )


with col6:

    st.subheader(
        "Accuracy Heatmap"
    )

    heatmap_df = (
        performance_df
        .pivot_table(
            index="Halb",
            columns="Model Used",
            values="Accuracy",
            aggfunc="mean"
        )
    )

    heatmap_df = (
        heatmap_df
        .fillna(0)
        .head(25)
    )

    fig_heat = px.imshow(
        heatmap_df,
        aspect="auto",
        color_continuous_scale="RdYlGn",
        text_auto=".0f"
    )

    fig_heat.update_layout(
        height=700
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )


# =====================================================
# ROW 2
# =====================================================

st.markdown("---")

col7, col8 = st.columns(2)

with col7:

    st.subheader(
        "Accuracy Comparison"
    )

    fig_acc = px.bar(
        leaderboard,
        x="Model Used",
        y="Accuracy",
        color="Accuracy",
        color_continuous_scale="Blues"
    )

    fig_acc.update_layout(
        height=500,
        template="plotly_dark",
        xaxis_title="Forecast Model",
        yaxis_title="Accuracy (%)"
    )

    st.plotly_chart(
        fig_acc,
        use_container_width=True
    )


with col8:

    st.subheader(
        "MAPE Comparison"
    )

    fig_mape = px.bar(
        leaderboard,
        x="Model Used",
        y="MAPE",
        color="MAPE",
        color_continuous_scale="Reds"
    )

    fig_mape.update_layout(
        height=500,
        template="plotly_dark",
        xaxis_title="Forecast Model",
        yaxis_title="MAPE"
    )

    st.plotly_chart(
        fig_mape,
        use_container_width=True
    )


# =====================================================
# BEST MODEL
# =====================================================

st.markdown("---")

best_model = leaderboard.iloc[0]

st.success(
    f"""
🏆 Best Forecast Model: {best_model['Model Used']}

Accuracy: {best_model['Accuracy']:.2f}%

MAPE: {best_model['MAPE']:.2f}

MAE: {best_model['MAE']:.2f}
"""
)


# =====================================================
# MODEL RANKING
# =====================================================

st.markdown("---")

st.subheader(
    "Model Ranking"
)

ranking_df = leaderboard.copy()

ranking_df["Rank"] = range(
    1,
    len(ranking_df) + 1
)

ranking_df = ranking_df[
    [
        "Rank",
        "Model Used",
        "Accuracy",
        "MAPE",
        "MAE"
    ]
]

st.dataframe(
    ranking_df,
    use_container_width=True
)


# =====================================================
# DETAILED PERFORMANCE TABLE
# =====================================================

st.markdown("---")

st.subheader(
    "Detailed Forecast Performance"
)

detail_df = performance_df[
    [
        "Halb",
        "engine_type",
        "map_model",
        "Vehicle_Type",
        "Model Used",
        "Accuracy",
        "MAPE",
        "MAE"
    ]
].copy()

detail_df.columns = [
    "HALB",
    "Engine",
    "Model",
    "Vehicle Type",
    "Forecast Model",
    "Accuracy %",
    "MAPE",
    "MAE"
]

st.dataframe(
    detail_df,
    use_container_width=True,
    height=500
)