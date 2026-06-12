import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Forecast Explorer",
    layout="wide"
)

st.title("🔍 Forecast Explorer")

# =====================================
# LOAD DATA
# =====================================

model_files = {

    "Moving Average":
        "outputs/moving_average_results.xlsx",

    "SES":
        "outputs/ses_results.xlsx",

    "Holt":
        "outputs/holt_results.xlsx",

    "ARIMA":
        "outputs/arima_results.xlsx",

    "Recursive Linear Regression":
        "outputs/recursive_linear_regression_results.xlsx"

}

selected_model = st.selectbox(
    "Select Forecast Model",
    list(model_files.keys())
)
st.success(
    f"Currently Viewing: {selected_model}"
)

df = pd.read_excel(
    model_files[selected_model]
)

# =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.header("Filters")

halb = st.sidebar.selectbox(
    "HALB",
    sorted(df["Halb"].astype(str).unique())
)

filtered_df = df[
    df["Halb"].astype(str) == halb
]

engine_type = st.sidebar.selectbox(
    "Engine Type",
    sorted(filtered_df["engine_type"].astype(str).unique())
)

filtered_df = filtered_df[
    filtered_df["engine_type"].astype(str)
    == engine_type
]

map_model = st.sidebar.selectbox(
    "Map Model",
    sorted(filtered_df["map_model"].astype(str).unique())
)

filtered_df = filtered_df[
    filtered_df["map_model"].astype(str)
    == map_model
]

vehicle_type = st.sidebar.selectbox(
    "Vehicle Type",
    sorted(filtered_df["Vehicle_Type"].astype(str).unique())
)

filtered_df = filtered_df[
    filtered_df["Vehicle_Type"].astype(str)
    == vehicle_type
]

# =====================================
# SELECTED ROW
# =====================================

if len(filtered_df) == 0:

    st.warning(
        "No matching series found."
    )

else:

    row = filtered_df.iloc[0]

    st.info(
        f"""
        HALB: {halb}

        Engine: {engine_type}

        Model: {map_model}

        Vehicle Type: {vehicle_type}
        """
    )

    st.subheader(
        f"Selected Forecast Series ({selected_model})"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "MAE",
            round(row["MAE"], 2)
        )

    with col2:
        st.metric(
            "MAPE",
            round(row["MAPE"], 2)
        )

    with col3:
        st.metric(
            "Accuracy",
            f"{round(row['Accuracy'],2)}%"
        )

    # =====================================
    # TABLE
    # =====================================

    result_table = pd.DataFrame(
        {
            "Month": [
                "Jan-2025",
                "Feb-2025",
                "Mar-2025"
            ],

            "Actual": [
                row["Jan_Actual"],
                row["Feb_Actual"],
                row["Mar_Actual"]
            ],

            "Forecast": [
                round(row["Jan_Forecast"], 2),
                round(row["Feb_Forecast"], 2),
                round(row["Mar_Forecast"], 2)
            ]
        }
    )
    result_table["Error"] = (
        result_table["Actual"]
        -
        result_table["Forecast"]
    ).abs()

    st.markdown("---")

    st.subheader(
        "Actual vs Forecast"
    )

    st.dataframe(
        result_table,
        use_container_width=True
    )

    # =====================================
    # BAR CHART
    # =====================================

    chart_df = result_table.melt(
        id_vars="Month",
        value_vars=[
            "Actual",
            "Forecast"
        ]
    )

    fig = px.bar(
        chart_df,
        x="Month",
        y="value",
        color="variable",
        barmode="group",
        title="Actual vs Forecast"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================
    # LINE CHART
    # =====================================

    fig2 = px.line(
        result_table,
        x="Month",
        y=[
            "Actual",
            "Forecast"
        ],
        markers=True,
        title="Forecast Trend"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )