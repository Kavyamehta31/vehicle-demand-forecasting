import pandas as pd

from src.feature_engineering import (
    create_time_series_features
)

from src.ml_models import (
    linear_regression_forecast,
    random_forest_forecast,
    xgboost_forecast
)


def get_ml_forecast(
    train,
    test,
    model_name
):

    if model_name == "linear_regression":

        return linear_regression_forecast(
            train,
            test
        )

    elif model_name == "random_forest":

        return random_forest_forecast(
            train,
            test
        )

    elif model_name == "xgboost":

        return xgboost_forecast(
            train,
            test
        )

    else:

        raise ValueError(
            f"Unknown ML Model: {model_name}"
        )


def run_ml_model_for_all_series(
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

        try:

            group = group.sort_values(
                "Month"
            )

            feature_df = (
                create_time_series_features(
                    group
                )
            )

            train = feature_df[
                feature_df["Month"]
                < "2025-01-01"
            ]

            test = feature_df[
                feature_df["Month"]
                >= "2025-01-01"
            ]

            if len(test) != 3:
                continue

            forecast = get_ml_forecast(
                train,
                test,
                model_name
            )

            result_row = {

                "Halb": keys[0],
                "engine_type": keys[1],
                "map_model": keys[2],
                "Vehicle_Type": keys[3],

                "Jan_Actual":
                    test.iloc[0]["total_demand"],

                "Jan_Forecast":
                    max(
                        0,
                        forecast[0]
                    ),

                "Feb_Actual":
                    test.iloc[1]["total_demand"],

                "Feb_Forecast":
                    max(
                        0,
                        forecast[1]
                    ),

                "Mar_Actual":
                    test.iloc[2]["total_demand"],

                "Mar_Forecast":
                    max(
                        0,
                        forecast[2]
                    )

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
# MAE
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


    # ==========================
    # MAPE
    # ==========================

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


    # ==========================
    # ACCURACY
    # ==========================

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