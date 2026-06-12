import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Forecast Analytics",
    layout="wide"
)

st.title("📈 Forecast Analytics")

# ==================================
# LOAD DATA
# ==================================

df = pd.read_excel(
    "outputs/recursive_linear_regression_results.xlsx"
)

# ==================================
# TOP KPI
# ==================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Series",
        len(df)
    )

with col2:
    st.metric(
        "Average Accuracy",
        f"{df['Accuracy'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Average MAE",
        f"{df['MAE'].mean():.2f}"
    )

st.markdown("---")

# ==================================
# TOP 10 BEST SERIES
# ==================================

st.subheader("🏆 Top 10 Best Forecasted Series")

best_df = (
    df.sort_values(
        by="Accuracy",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    best_df[
        [
            "Halb",
            "engine_type",
            "map_model",
            "Vehicle_Type",
            "Accuracy"
        ]
    ],
    use_container_width=True
)

# ==================================
# TOP 10 WORST SERIES
# ==================================

st.subheader("⚠️ Top 10 Worst Forecasted Series")

worst_df = (
    df.sort_values(
        by="Accuracy",
        ascending=True
    )
    .head(10)
)

st.dataframe(
    worst_df[
        [
            "Halb",
            "engine_type",
            "map_model",
            "Vehicle_Type",
            "Accuracy"
        ]
    ],
    use_container_width=True
)

# ==================================
# ACCURACY DISTRIBUTION
# ==================================

st.subheader("📊 Accuracy Distribution")

fig = px.histogram(
    df,
    x="Accuracy",
    nbins=20
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# VEHICLE TYPE PERFORMANCE
# ==================================

st.subheader("🚚 Vehicle Type Performance")

vehicle_perf = (
    df.groupby(
        "Vehicle_Type"
    )["Accuracy"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    vehicle_perf,
    x="Vehicle_Type",
    y="Accuracy",
    text="Accuracy"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)