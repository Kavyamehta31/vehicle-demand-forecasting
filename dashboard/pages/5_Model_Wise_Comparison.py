import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Model Wise Comparison",
    layout="wide"
)

st.title("🏆 Model Wise Comparison")

# ==================================
# LOAD FILES
# ==================================

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

dataframes = {}

for model_name, file_path in model_files.items():

    dataframes[model_name] = pd.read_excel(
        file_path
    )

# ==================================
# FILTERS
# ==================================

base_df = dataframes[
    "Moving Average"
]

halb = st.sidebar.selectbox(
    "HALB",
    sorted(
        base_df["Halb"]
        .astype(str)
        .unique()
    )
)

filtered = base_df[
    base_df["Halb"]
    .astype(str)
    == halb
]

engine_type = st.sidebar.selectbox(
    "Engine Type",
    sorted(
        filtered["engine_type"]
        .astype(str)
        .unique()
    )
)

filtered = filtered[
    filtered["engine_type"]
    .astype(str)
    == engine_type
]

map_model = st.sidebar.selectbox(
    "Map Model",
    sorted(
        filtered["map_model"]
        .astype(str)
        .unique()
    )
)

filtered = filtered[
    filtered["map_model"]
    .astype(str)
    == map_model
]

vehicle_type = st.sidebar.selectbox(
    "Vehicle Type",
    sorted(
        filtered["Vehicle_Type"]
        .astype(str)
        .unique()
    )
)

# ==================================
# SERIES INFO
# ==================================

st.info(
    f"""
    HALB: {halb}

    Engine: {engine_type}

    Model: {map_model}

    Vehicle Type: {vehicle_type}
    """
)

# ==================================
# COMPARISON TABLE
# ==================================

comparison_rows = []

for model_name, df in dataframes.items():

    temp = df[
        (df["Halb"].astype(str) == halb)
        &
        (
            df["engine_type"]
            .astype(str)
            == engine_type
        )
        &
        (
            df["map_model"]
            .astype(str)
            == map_model
        )
        &
        (
            df["Vehicle_Type"]
            .astype(str)
            == vehicle_type
        )
    ]

    if len(temp) == 0:
        continue

    row = temp.iloc[0]

    comparison_rows.append(
        {

            "Model":
                model_name,

            "Jan Forecast":
                round(
                    row["Jan_Forecast"],
                    2
                ),

            "Feb Forecast":
                round(
                    row["Feb_Forecast"],
                    2
                ),

            "Mar Forecast":
                round(
                    row["Mar_Forecast"],
                    2
                ),

            "MAE":
                round(
                    row["MAE"],
                    2
                ),

            "MAPE":
                round(
                    row["MAPE"],
                    2
                ),

            "Accuracy":
                round(
                    row["Accuracy"],
                    2
                )

        }
    )

comparison_df = pd.DataFrame(
    comparison_rows
)

st.subheader(
    "Model Forecast Comparison"
)

st.dataframe(
    comparison_df,
    use_container_width=True
)

# ==================================
# BEST MODEL
# ==================================

best_model = (
    comparison_df
    .sort_values(
        by="Accuracy",
        ascending=False
    )
    .iloc[0]
)

st.success(
    f"""
    Best Model: {best_model['Model']}

    Accuracy: {best_model['Accuracy']}%
    """
)