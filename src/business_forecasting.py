import pandas as pd

from src.statistical_models import holt_forecast


def forecast_active_series(df):

    results = []

    grouped = df.groupby(
        [
            "Halb",
            "engine_type",
            "map_model",
            "Vehicle_Type"
        ]
    )

    for keys, group in grouped:

        total_demand = group["total_demand"].sum()

        # Skip intermittent series
        if total_demand < 50:
            continue

        group = group.sort_values("Month")

        train = group[
            group["Month"] < "2025-01-01"
        ]

        test = group[
            group["Month"] >= "2025-01-01"
        ]

        forecast = holt_forecast(
            train,
            periods=3
        )
        forecast = forecast.clip(lower=0)

        result_row = {
            "Halb": keys[0],
            "engine_type": keys[1],
            "map_model": keys[2],
            "Vehicle_Type": keys[3],

            "Jan_Actual": test.iloc[0]["total_demand"],
            "Jan_Forecast": forecast.iloc[0],

            "Feb_Actual": test.iloc[1]["total_demand"],
            "Feb_Forecast": forecast.iloc[1],

            "Mar_Actual": test.iloc[2]["total_demand"],
            "Mar_Forecast": forecast.iloc[2]
        }

        results.append(result_row)

    results_df = pd.DataFrame(results)
    results_df["Jan_Error"] = abs(
        results_df["Jan_Actual"]
        - results_df["Jan_Forecast"]
    )

    results_df["Feb_Error"] = abs(
        results_df["Feb_Actual"]
        - results_df["Feb_Forecast"]
    )

    results_df["Mar_Error"] = abs(
        results_df["Mar_Actual"]
        - results_df["Mar_Forecast"]
    )
    import numpy as np

    results_df["Jan_APE"] = np.where(
        results_df["Jan_Actual"] == 0,
        0,
        abs(
            (results_df["Jan_Actual"] - results_df["Jan_Forecast"])
            / results_df["Jan_Actual"]
        ) * 100
    )

    results_df["Feb_APE"] = np.where(
        results_df["Feb_Actual"] == 0,
        0,
        abs(
            (results_df["Feb_Actual"] - results_df["Feb_Forecast"])
            / results_df["Feb_Actual"]
        ) * 100
    )

    results_df["Mar_APE"] = np.where(
        results_df["Mar_Actual"] == 0,
        0,
        abs(
            (results_df["Mar_Actual"] - results_df["Mar_Forecast"])
            / results_df["Mar_Actual"]
        ) * 100
    )
    return results_df