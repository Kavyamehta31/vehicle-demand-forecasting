import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_main_data
from utils.filters import create_filters


# =====================================
# PAGE TITLE
# =====================================

st.title("🔍 Exploratory Data Analysis (EDA)")


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
        "Records",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Total Demand",
        f"{int(filtered_df['demand'].sum()):,}"
    )

with col3:
    st.metric(
        "Average Demand",
        round(filtered_df["demand"].mean(), 2)
    )

with col4:
    st.metric(
        "Max Demand",
        int(filtered_df["demand"].max())
    )


# =====================================
# ROW 1
# VEHICLE TYPE + ENGINE TYPE
# =====================================

st.markdown("---")

col5, col6 = st.columns(2)

with col5:

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
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_vehicle,
        use_container_width=True
    )


with col6:

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
        template="plotly_dark"
    )

    fig_engine.update_yaxes(
        categoryorder="total ascending"
    )

    st.plotly_chart(
        fig_engine,
        use_container_width=True
    )


# =====================================
# ROW 2
# TOP MODELS + TOP HALBS
# =====================================

st.markdown("---")

col7, col8 = st.columns(2)

with col7:

    st.subheader(
        "Top 15 Models by Demand"
    )

    model_df = (
        filtered_df
        .groupby("map_model")["demand"]
        .sum()
        .reset_index()
        .sort_values(
            "demand",
            ascending=False
        )
        .head(15)
    )

    fig_model = px.bar(
        model_df,
        x="demand",
        y="map_model",
        orientation="h",
        color="demand"
    )

    fig_model.update_layout(
        height=500,
        template="plotly_dark"
    )

    fig_model.update_yaxes(
        categoryorder="total ascending"
    )

    st.plotly_chart(
        fig_model,
        use_container_width=True
    )


with col8:

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
        .head(15)
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
# DEMAND DISTRIBUTION
# =====================================

st.markdown("---")

st.subheader(
    "Demand Distribution"
)

fig_hist = px.histogram(
    filtered_df,
    x="demand",
    nbins=40,
    color_discrete_sequence=["#4F46E5"]
)

fig_hist.update_layout(
    height=500,
    template="plotly_dark",
    xaxis_title="Demand",
    yaxis_title="Frequency"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)


# =====================================
# ROW 4
# DEMAND BOXPLOT
# =====================================

st.markdown("---")

st.subheader(
    "Demand Outlier Analysis"
)

fig_box = px.box(
    filtered_df,
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
# SUMMARY TABLE
# =====================================

st.markdown("---")

st.subheader(
    "EDA Summary"
)

summary_df = pd.DataFrame(
    {
        "Metric": [
            "Total Records",
            "Total Demand",
            "Average Demand",
            "Maximum Demand",
            "Vehicle Types",
            "Engine Types",
            "Models",
            "HALBs"
        ],
        "Value": [
            len(filtered_df),
            int(filtered_df["demand"].sum()),
            round(filtered_df["demand"].mean(), 2),
            int(filtered_df["demand"].max()),
            filtered_df["Vehicle_Type"].nunique(),
            filtered_df["engine_type"].nunique(),
            filtered_df["map_model"].nunique(),
            filtered_df["Halb"].nunique()
        ]
    }
)

st.dataframe(
    summary_df,
    use_container_width=True
)