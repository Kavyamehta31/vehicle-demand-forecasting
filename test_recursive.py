from src.data_preprocessing import (
    load_data
)

from src.ml_recursive_forecasting import (
    recursive_linear_regression_forecast
)

# ==========================
# LOAD DATA
# ==========================

df = load_data(
    "data/final_data_for_vehicle_forecasting.csv"
)

# ==========================
# GET FIRST SERIES
# ==========================

grouped = df.groupby(
    [
        "Halb",
        "engine_type",
        "map_model",
        "Vehicle_Type"
    ]
)

for keys, series in grouped:

    actual = series[
        series["Month"] >= "2025-01-01"
    ]["total_demand"].sum()

    counter = 0

for keys, series in grouped:

    actual = series[
        series["Month"] >= "2025-01-01"
    ]["total_demand"].sum()

    if actual > 0:

        forecast = (
            recursive_linear_regression_forecast(
                series
            )
        )

        print("\nSERIES")
        print(keys)

        print("FORECAST")
        print(forecast)

        print("ACTUAL")
        print(
            series[
                series["Month"] >= "2025-01-01"
            ]["total_demand"].tolist()
        )

        counter += 1

        if counter == 5:
            break

# ==========================
# FORECAST
# ==========================

forecast = (
    recursive_linear_regression_forecast(
        series
    )
)

# ==========================
# ACTUALS
# ==========================

actual = series[
    series["Month"] >= "2025-01-01"
]["total_demand"].tolist()

print("\nSERIES")

print(keys)

print("\nFORECAST")

print(forecast)

print("\nACTUAL")

print(actual)