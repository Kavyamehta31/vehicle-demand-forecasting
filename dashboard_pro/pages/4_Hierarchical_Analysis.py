import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_main_data
from utils.filters import create_filters


# =====================================
# PAGE TITLE
# =====================================

st.title("🌳 Hierarchical Analysis")


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
# KPI SECTION
# =====================================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Vehicle Types",
        filtered_df["Vehicle_Type"].nunique()
    )

with col2:
    st.metric(
        "Engine Types",
        filtered_df["engine_type"].nunique()
    )

with col3:
    st.metric(
        "Models",
        filtered_df["map_model"].nunique()
    )

with col4:
    st.metric(
        "HALBs",
        filtered_df["Halb"].nunique()
    )


# =====================================
# SUNBURST + TREEMAP
# =====================================

st.markdown("---")

col5, col6 = st.columns(2)

with col5:

    st.subheader(
        "Vehicle → Engine → Model → HALB"
    )

    fig_sunburst = px.sunburst(
        filtered_df,
        path=[
            "Vehicle_Type",
            "engine_type",
            "map_model",
            "Halb"
        ],
        values="demand"
    )

    fig_sunburst.update_layout(
        height=700,
        template="plotly_white"
    )

    st.plotly_chart(
        fig_sunburst,
        use_container_width=True
    )

with col6:

    st.subheader(
        "Treemap Hierarchy"
    )

    fig_tree = px.treemap(
        filtered_df,
        path=[
            "Vehicle_Type",
            "engine_type",
            "map_model"
        ],
        values="demand"
    )

    fig_tree.update_layout(
        height=700,
        template="plotly_white"
    )

    st.plotly_chart(
        fig_tree,
        use_container_width=True
    )


# =====================================
# VEHICLE VS ENGINE
# =====================================

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
        .sort_values(
            "demand",
            ascending=False
        )
    )

    fig_vehicle = px.bar(
        vehicle_df,
        x="Vehicle_Type",
        y="demand",
        color="demand"
    )

    fig_vehicle.update_layout(
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(
        fig_vehicle,
        use_container_width=True
    )


with col8:

    st.subheader(
        "Top Engine Types"
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
        height=500,
        template="plotly_white"
    )

    fig_engine.update_yaxes(
        categoryorder="total ascending"
    )

    st.plotly_chart(
        fig_engine,
        use_container_width=True
    )


# =====================================
# HIERARCHICAL TABLE
# =====================================

st.markdown("---")

st.subheader(
    "Vehicle → Engine → Model Summary"
)

hierarchy_df = (
    filtered_df
    .groupby(
        [
            "Vehicle_Type",
            "engine_type",
            "map_model"
        ]
    )["demand"]
    .sum()
    .reset_index()
    .sort_values(
        "demand",
        ascending=False
    )
)

st.dataframe(
    hierarchy_df,
    use_container_width=True,
    height=500
)


# =====================================
# TOP HALBs
# =====================================

st.markdown("---")

st.subheader(
    "Top HALBs by Demand"
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
    height=600,
    template="plotly_white"
)

fig_halb.update_yaxes(
    categoryorder="total ascending"
)

st.plotly_chart(
    fig_halb,
    use_container_width=True
)


# =====================================
# BUSINESS INSIGHTS
# =====================================

st.markdown("---")

st.subheader(
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
    ✔ Highest demand vehicle category: {top_vehicle}

    ✔ Highest demand engine type: {top_engine}

    ✔ Highest demand model: {top_model}

    ✔ Hierarchical analysis completed successfully.
    """
)