import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from utils.data_loader import load_main_data
from utils.filters import create_filters


# =====================================================
# PAGE TITLE
# =====================================================

st.title("📈 Advanced Analytics")


# =====================================================
# LOAD DATA
# =====================================================

df = load_main_data()


# =====================================================
# FILTERS
# =====================================================

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


# =====================================================
# KPI CARDS
# =====================================================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Demand",
    f"{int(filtered_df['demand'].sum()):,}"
)

col2.metric(
    "HALBs",
    filtered_df["Halb"].nunique()
)

col3.metric(
    "Models",
    filtered_df["map_model"].nunique()
)

col4.metric(
    "Vehicle Types",
    filtered_df["Vehicle_Type"].nunique()
)


# =====================================================
# TOP SECTION
# =====================================================

st.markdown("---")

st.header("Top Demand Contributors")

col5, col6 = st.columns(2)

# =====================================================
# TREEMAP
# =====================================================

with col5:

    st.subheader(
        "Top Demand Contributors (Treemap)"
    )

    treemap_df = (
        filtered_df
        .groupby(
            ["Halb", "map_model"]
        )["demand"]
        .sum()
        .reset_index()
    )

    fig_tree = px.treemap(
        treemap_df,
        path=["Halb", "map_model"],
        values="demand",
        color="demand",
        color_continuous_scale="Blues"
    )

    fig_tree.update_layout(
        height=650
    )

    st.plotly_chart(
        fig_tree,
        use_container_width=True
    )


# =====================================================
# PARETO
# =====================================================

with col6:

    st.subheader(
        "Pareto Analysis (Models)"
    )

    pareto_df = (
        filtered_df
        .groupby("map_model")["demand"]
        .sum()
        .reset_index()
        .sort_values(
            "demand",
            ascending=False
        )
    )

    pareto_df["cum_pct"] = (
        pareto_df["demand"].cumsum()
        /
        pareto_df["demand"].sum()
        * 100
    )

    fig_pareto = px.bar(
        pareto_df,
        x="map_model",
        y="demand"
    )

    fig_pareto.add_scatter(
        x=pareto_df["map_model"],
        y=pareto_df["cum_pct"],
        mode="lines",
        name="Cumulative %"
    )

    fig_pareto.update_layout(
        height=650,
        xaxis_title="Model",
        yaxis_title="Demand"
    )

    st.plotly_chart(
        fig_pareto,
        use_container_width=True
    )


# =====================================================
# VEHICLE TYPE ANALYSIS
# =====================================================

st.markdown("---")

col7, col8 = st.columns(2)

with col7:

    st.subheader(
        "Demand by Vehicle Type"
    )

    vehicle_df = (
        filtered_df
        .groupby("Vehicle_Type")["demand"]
        .sum()
        .reset_index()
    )

    fig_vehicle = px.pie(
        vehicle_df,
        names="Vehicle_Type",
        values="demand",
        hole=0.5
    )

    fig_vehicle.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_vehicle,
        use_container_width=True
    )


with col8:

    st.subheader(
        "Demand by Engine Type"
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
        .head(15)
    )

    fig_engine = px.bar(
        engine_df,
        x="demand",
        y="engine_type",
        orientation="h",
        color="demand"
    )

    fig_engine.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_engine,
        use_container_width=True
    )


# =====================================================
# DEMAND CONCENTRATION
# =====================================================

st.markdown("---")

st.subheader(
    "Demand Concentration Analysis"
)

top10 = (
    filtered_df
    .groupby("Halb")["demand"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .sum()
)

total_demand = (
    filtered_df["demand"].sum()
)

concentration = (
    top10
    /
    total_demand
    * 100
)

st.info(
    f"""
Top 10 HALBs contribute
{concentration:.2f}% of total demand.
"""
)


# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.markdown("---")

st.header(
    "Business Insights"
)

top_vehicle = (
    filtered_df
    .groupby("Vehicle_Type")["demand"]
    .sum()
    .idxmax()
)

top_engine = (
    filtered_df
    .groupby("engine_type")["demand"]
    .sum()
    .idxmax()
)

top_model = (
    filtered_df
    .groupby("map_model")["demand"]
    .sum()
    .idxmax()
)

st.success(
    f"""
🚚 Highest Demand Vehicle Type: {top_vehicle}

⚙ Highest Demand Engine Type: {top_engine}

🏆 Highest Demand Model: {top_model}

📈 Demand concentration among top HALBs is
{concentration:.2f}%.
"""
)