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

st.title("📈 Forecast Comparison")


# =====================================
# LOAD MAIN DATA
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
# LOAD MODEL COMPARISON FILE
# =====================================

comparison_df = pd.read_excel(
    "outputs/master_model_comparison.xlsx"
)


# =====================================
# KPI SECTION
# =====================================

best_accuracy_row = comparison_df.loc[
    comparison_df["Average_Accuracy"].idxmax()
]

best_mae_row = comparison_df.loc[
    comparison_df["Average_MAE"].idxmin()
]

best_model = best_accuracy_row["Model"]

highest_accuracy = round(
    best_accuracy_row["Average_Accuracy"],
    2
)

lowest_mae = round(
    best_mae_row["Average_MAE"],
    2
)

total_models = len(comparison_df)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Best Model",
        best_model
    )

with col2:
    st.metric(
        "Highest Accuracy",
        f"{highest_accuracy}%"
    )

with col3:
    st.metric(
        "Lowest MAE",
        lowest_mae
    )

with col4:
    st.metric(
        "Models Compared",
        total_models
    )


# =====================================
# ROW 1
# ACCURACY + MAE
# =====================================

st.markdown("---")

col5, col6 = st.columns(2)

with col5:

    st.subheader(
        "🎯 Accuracy Comparison"
    )

    accuracy_df = comparison_df.sort_values(
        "Average_Accuracy",
        ascending=False
    )

    fig_acc = px.bar(
        accuracy_df,
        x="Model",
        y="Average_Accuracy",
        color="Average_Accuracy",
        text="Average_Accuracy"
    )

    fig_acc.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_acc.update_layout(
        height=500,
        template="plotly_dark",
        xaxis_title="Model",
        yaxis_title="Average Accuracy (%)"
    )

    st.plotly_chart(
        fig_acc,
        use_container_width=True
    )

with col6:

    st.subheader(
        "📉 MAE Comparison"
    )

    mae_df = comparison_df.sort_values(
        "Average_MAE",
        ascending=True
    )

    fig_mae = px.bar(
        mae_df,
        x="Model",
        y="Average_MAE",
        color="Average_MAE",
        text="Average_MAE"
    )

    fig_mae.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_mae.update_layout(
        height=500,
        template="plotly_dark",
        xaxis_title="Model",
        yaxis_title="Average MAE"
    )

    st.plotly_chart(
        fig_mae,
        use_container_width=True
    )


# =====================================
# ROW 2
# MODEL RANKING + SCATTER
# =====================================

st.markdown("---")

col7, col8 = st.columns(2)

with col7:

    st.subheader(
        "🏆 Model Ranking"
    )

    ranking_df = comparison_df.copy()

    ranking_df = ranking_df.sort_values(
        "Average_Accuracy",
        ascending=False
    )

    ranking_df.insert(
        0,
        "Rank",
        range(1, len(ranking_df) + 1)
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

with col8:

    st.subheader(
        "📍 Accuracy vs MAE"
    )

    fig_scatter = px.scatter(
        comparison_df,
        x="Average_MAE",
        y="Average_Accuracy",
        color="Model",
        size="Average_Accuracy",
        text="Model"
    )

    fig_scatter.update_traces(
        textposition="top center"
    )

    fig_scatter.update_layout(
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


# =====================================
# ROW 3
# FULL COMPARISON TABLE
# =====================================

st.markdown("---")

st.subheader(
    "📋 Forecast Comparison Table"
)

st.dataframe(
    comparison_df,
    use_container_width=True
)


# =====================================
# ROW 4
# BUSINESS INSIGHTS
# =====================================

st.markdown("---")

st.subheader(
    "💡 Business Insights"
)

st.success(
    f"""
    ✓ Best Forecasting Model: {best_model}

    ✓ Highest Accuracy Achieved: {highest_accuracy:.2f}%

    ✓ Lowest Forecast Error (MAE): {lowest_mae:.2f}

    ✓ {total_models} forecasting models compared

    ✓ Forecast comparison completed successfully
    """
)