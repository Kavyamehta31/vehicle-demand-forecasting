import pandas as pd

from src.statistical_models import (
    moving_average_forecast,
    ses_forecast,
    holt_forecast
)

from src.arima_models import (
    arima_forecast
)


def get_forecast(
    train,
    model_name,
    periods=3
):

    if model_name == "moving_average":
        return moving_average_forecast(
            train,
            periods
        )

    elif model_name == "ses":
        return ses_forecast(
            train,
            periods
        )

    elif model_name == "holt":
        return holt_forecast(
            train,
            periods
        )

    elif model_name == "arima":
        return arima_forecast(
            train,
            periods
        )

    else:
        raise ValueError(
            f"Unknown Model: {model_name}"
        )


def run_model_for_all_series(
    df,
    model_name
):

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

        group = group.sort_values(
            "Month"
        )

        train = group[
            group["Month"] < "2025-01-01"
        ]

        test = group[
            group["Month"] >= "2025-01-01"
        ]

        try:

            forecast = get_forecast(
                train,
                model_name,
                periods=3
            )

            forecast = forecast.clip(
                lower=0
            )

            result_row = {

                "Halb": keys[0],
                "engine_type": keys[1],
                "map_model": keys[2],
                "Vehicle_Type": keys[3],

                "Jan_Actual":
                    test.iloc[0]["total_demand"],

                "Jan_Forecast":
                    forecast.iloc[0],

                "Feb_Actual":
                    test.iloc[1]["total_demand"],

                "Feb_Forecast":
                    forecast.iloc[1],

                "Mar_Actual":
                    test.iloc[2]["total_demand"],

                "Mar_Forecast":
                    forecast.iloc[2]

            }

            results.append(
                result_row
            )

        except Exception:
            continue

    results_df = pd.DataFrame(
        results
    )

    # ==========================
    # ERROR CALCULATIONS
    # ==========================

    results_df["MAE"] = (

        abs(
            results_df["Jan_Actual"]
            - results_df["Jan_Forecast"]
        )

        +

        abs(
            results_df["Feb_Actual"]
            - results_df["Feb_Forecast"]
        )

        +

        abs(
            results_df["Mar_Actual"]
            - results_df["Mar_Forecast"]
        )

    ) / 3

    results_df["MAPE"] = (

        (

            abs(
                results_df["Jan_Actual"]
                - results_df["Jan_Forecast"]
            )

            /

            results_df["Jan_Actual"]
            .replace(0, 1)

        )

        +

        (

            abs(
                results_df["Feb_Actual"]
                - results_df["Feb_Forecast"]
            )

            /

            results_df["Feb_Actual"]
            .replace(0, 1)

        )

        +

        (

            abs(
                results_df["Mar_Actual"]
                - results_df["Mar_Forecast"]
            )

            /

            results_df["Mar_Actual"]
            .replace(0, 1)

        )

    ) * 100 / 3

    results_df["Accuracy"] = (
        100
        -
        results_df["MAPE"]
    )

    results_df["Accuracy"] = (
        results_df["Accuracy"]
        .clip(lower=0)
    )

    return results_df