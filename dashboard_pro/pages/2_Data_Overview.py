import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_main_data
from utils.filters import create_filters
from utils.theme import load_css

load_css()

# =====================================
# PAGE TITLE
# =====================================

st.title("📈 Data Overview")


# =====================================
# LOAD DATA
# =====================================

df = load_main_data()


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
# NON-ZERO DEMAND DATA
# =====================================

non_zero_df = filtered_df[
    filtered_df["demand"] > 0
].copy()


# =====================================
# ROW 1
# HISTOGRAM + BOXPLOT
# =====================================

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Demand Distribution (Non-Zero)"
    )

    fig_hist = px.histogram(
        non_zero_df,
        x="demand",
        nbins=30
    )

    fig_hist.update_layout(
        height=500,
        template="plotly_dark",
        xaxis_title="Demand",
        yaxis_title="Count"
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

with col2:

    st.subheader(
        "Demand Box Plot"
    )

    fig_box = px.box(
        non_zero_df,
        y="demand"
    )

    fig_box.update_layout(
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_box,
        use_container_width=True
    )


# =====================================
# ROW 2
# MONTHLY TREND + TOP HALB
# =====================================

st.markdown("---")

col3, col4 = st.columns(2)

with col3:

    st.subheader(
        "Monthly Demand Trend"
    )

    # CHANGE THIS COLUMN NAME IF NEEDED
    date_col = "Month"

    monthly_df = filtered_df.copy()

    monthly_df[date_col] = pd.to_datetime(
        monthly_df[date_col]
    )

    monthly_df = (
        monthly_df
        .groupby(
            monthly_df[date_col].dt.to_period("M")
        )["demand"]
        .sum()
        .reset_index()
    )

    monthly_df[date_col] = (
        monthly_df[date_col]
        .astype(str)
    )

    monthly_df = monthly_df.sort_values(
        date_col
    )

    fig_month = px.line(
        monthly_df,
        x=date_col,
        y="demand",
        markers=True
    )

    fig_month.update_layout(
        height=500,
        template="plotly_dark",
        xaxis_title="Month",
        yaxis_title="Demand"
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

with col4:

    st.subheader(
        "Top 20 by Demand — HALB"
    )

    halb_df = (
        filtered_df
        .groupby("Halb")["demand"]
        .sum()
        .reset_index()
        .sort_values(
            "demand",
            ascending=False
        )
        .head(20)
    )

    fig_halb = px.bar(
        halb_df,
        x="demand",
        y="Halb",
        orientation="h",
        color="demand"
    )

    fig_halb.update_layout(
        height=500,
        template="plotly_dark"
    )

    fig_halb.update_yaxes(
        categoryorder="total ascending"
    )

    st.plotly_chart(
        fig_halb,
        use_container_width=True
    )


# =====================================
# ROW 3
# TOP ENGINES + VEHICLE TYPES
# =====================================

st.markdown("---")

col5, col6 = st.columns(2)

with col5:

    st.subheader(
        "Top 20 by Demand — Engine"
    )

    engine_df = (
        filtered_df
        .groupby("engine_type")["demand"]
        .sum()
        .reset_index()
        .sort_values(
            "demand",
            ascending=False
        )
        .head(20)
    )

    fig_engine = px.bar(
        engine_df,
        x="demand",
        y="engine_type",
        orientation="h",
        color="demand"
    )

    fig_engine.update_layout(
        height=500,
        template="plotly_dark"
    )

    fig_engine.update_yaxes(
        categoryorder="total ascending"
    )

    st.plotly_chart(
        fig_engine,
        use_container_width=True
    )

with col6:

    st.subheader(
        "Demand by Vehicle Type"
    )

    vehicle_df = (
        filtered_df
        .groupby("Vehicle_Type")["demand"]
        .sum()
        .reset_index()
        .sort_values(
            "demand",
            ascending=False
        )
    )

    fig_vehicle = px.bar(
        vehicle_df,
        x="demand",
        y="Vehicle_Type",
        orientation="h",
        color="demand"
    )

    fig_vehicle.update_layout(
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_vehicle,
        use_container_width=True
    )