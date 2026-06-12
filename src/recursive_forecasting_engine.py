import pandas as pd

from src.ml_recursive_forecasting import (
    recursive_linear_regression_forecast
)


def run_recursive_linear_regression(df):

    results = []

    grouped = df.groupby(
        [
            "Halb",
            "engine_type",
            "map_model",
            "Vehicle_Type"
        ]
    )

    for keys, series in grouped:

        try:

            series = (
                series
                .sort_values("Month")
            )

            actuals = series[
                series["Month"] >= "2025-01-01"
            ]["total_demand"].tolist()

            if len(actuals) != 3:
                continue

            forecast = (
                recursive_linear_regression_forecast(
                    series
                )
            )

            jan_forecast = max(0, forecast[0])
            feb_forecast = max(0, forecast[1])
            mar_forecast = max(0, forecast[2])

            jan_actual = actuals[0]
            feb_actual = actuals[1]
            mar_actual = actuals[2]

            mae = (

                abs(jan_actual - jan_forecast)

                +

                abs(feb_actual - feb_forecast)

                +

                abs(mar_actual - mar_forecast)

            ) / 3

            mape = (

                (
                    abs(
                        jan_actual
                        - jan_forecast
                    )
                    /
                    max(1, jan_actual)
                )

                +

                (
                    abs(
                        feb_actual
                        - feb_forecast
                    )
                    /
                    max(1, feb_actual)
                )

                +

                (
                    abs(
                        mar_actual
                        - mar_forecast
                    )
                    /
                    max(1, mar_actual)
                )

            ) * 100 / 3

            accuracy = max(
                0,
                100 - mape
            )

            results.append(

                {

                    "Halb": keys[0],
                    "engine_type": keys[1],
                    "map_model": keys[2],
                    "Vehicle_Type": keys[3],

                    "Jan_Actual": jan_actual,
                    "Jan_Forecast": jan_forecast,

                    "Feb_Actual": feb_actual,
                    "Feb_Forecast": feb_forecast,

                    "Mar_Actual": mar_actual,
                    "Mar_Forecast": mar_forecast,

                    "MAE": mae,
                    "MAPE": mape,
                    "Accuracy": accuracy

                }

            )

        except Exception:
            continue

    return pd.DataFrame(results)