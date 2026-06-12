import streamlit as st
import pandas as pd

from utils.data_loader import load_main_data
from utils.filters import create_filters
from utils.theme import load_css

load_css()
# =====================================
# PAGE TITLE
# =====================================

st.title("💡 Business Insights")

# =====================================
# LOAD DATA
# =====================================

df = load_main_data()

model_df = pd.read_excel(
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
# MONTH PREP
# =====================================

filtered_df["Month"] = pd.to_datetime(
    filtered_df["Month"],
    dayfirst=True
)

# =====================================
# DEMAND INSIGHTS
# =====================================

top_halb = (
    filtered_df.groupby("Halb")["demand"]
    .sum()
    .idxmax()
)

top_halb_value = (
    filtered_df.groupby("Halb")["demand"]
    .sum()
    .max()
)

lowest_halb = (
    filtered_df.groupby("Halb")["demand"]
    .sum()
    .idxmin()
)

lowest_halb_value = (
    filtered_df.groupby("Halb")["demand"]
    .sum()
    .min()
)

top_model = (
    filtered_df.groupby("map_model")["demand"]
    .sum()
    .idxmax()
)

top_model_value = (
    filtered_df.groupby("map_model")["demand"]
    .sum()
    .max()
)

volatile_model = (
    filtered_df.groupby("map_model")["demand"]
    .std()
    .idxmax()
)

peak_month = (
    filtered_df.groupby(
        filtered_df["Month"].dt.to_period("M")
    )["demand"]
    .sum()
    .idxmax()
)

top_vehicle = (
    filtered_df.groupby("Vehicle_Type")["demand"]
    .sum()
    .idxmax()
)

# =====================================
# FORECAST INSIGHTS
# =====================================

best_model = model_df.loc[
    model_df["Average_Accuracy"].idxmax()
]

worst_model = model_df.loc[
    model_df["Average_Accuracy"].idxmin()
]

overall_accuracy = round(
    model_df["Average_Accuracy"].mean(),
    2
)

# =====================================
# TREND
# =====================================

monthly = (
    filtered_df.groupby(
        filtered_df["Month"].dt.to_period("M")
    )["demand"]
    .sum()
)

half = len(monthly) // 2

first_half = monthly.iloc[:half].sum()
second_half = monthly.iloc[half:].sum()

growth_pct = round(
    (
        (second_half - first_half)
        / max(first_half, 1)
    ) * 100,
    2
)

# =====================================
# PARETO
# =====================================

pareto_df = (
    filtered_df.groupby("map_model")["demand"]
    .sum()
    .sort_values(ascending=False)
)

cum_pct = (
    pareto_df.cumsum()
    / pareto_df.sum()
) * 100

pareto_models = (
    cum_pct <= 80
).sum()

# =====================================
# SECTION 1
# =====================================

st.header("📊 Demand Intelligence")

c1, c2, c3 = st.columns(3)

c1.metric(
    "🏆 Top Contributing HALB",
    str(top_halb),
    f"{int(top_halb_value):,} units"
)

c2.metric(
    "🚚 Top Performing Model",
    str(top_model),
    f"{int(top_model_value):,} units"
)

c3.metric(
    "⚡ Most Volatile Model",
    str(volatile_model)
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "⚠️ Lowest Demand HALB",
    str(lowest_halb),
    f"{int(lowest_halb_value):,} units"
)

c5.metric(
    "📈 Peak Demand Month",
    str(peak_month)
)

c6.metric(
    "🚛 Top Vehicle Type",
    str(top_vehicle)
)

# =====================================
# SECTION 2
# =====================================

st.header("🔮 Forecast Intelligence")

c7, c8, c9 = st.columns(3)

c7.metric(
    "✅ Best Forecast Model",
    best_model["Model"],
    f"{best_model['Average_Accuracy']:.2f}%"
)

c8.metric(
    "❌ Worst Forecast Model",
    worst_model["Model"],
    f"{worst_model['Average_Accuracy']:.2f}%"
)

c9.metric(
    "📊 Overall Accuracy",
    f"{overall_accuracy:.2f}%"
)

# =====================================
# SECTION 3
# =====================================

st.header("📈 Trend & Segment Intelligence")

c10, c11, c12 = st.columns(3)

c10.metric(
    "📉 Demand Growth",
    f"{growth_pct}%"
)

c11.metric(
    "📦 Active HALBs",
    filtered_df["Halb"].nunique()
)

c12.metric(
    "🌟 Pareto 80% Models",
    pareto_models
)

# =====================================
# EXECUTIVE SUMMARY
# =====================================

st.header("📝 Executive Summary")

st.success(
    f"""
    • Top demand contributor is HALB {top_halb}

    • Highest performing vehicle model is {top_model}

    • Best forecasting algorithm is {best_model['Model']}
      with {best_model['Average_Accuracy']:.2f}% accuracy

    • Peak demand occurred during {peak_month}

    • {pareto_models} models generate nearly 80% of demand

    • Demand growth over the period is {growth_pct}%
    """
)