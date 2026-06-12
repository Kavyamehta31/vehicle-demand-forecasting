import pandas as pd

from sklearn.linear_model import LinearRegression


FEATURE_COLUMNS = [
    "Lag_1",
    "Lag_2",
    "Lag_3",
    "Rolling_Mean_3"
]


def recursive_linear_regression_forecast(
    series
):

    series = (
        series
        .sort_values("Month")
        .copy()
    )

    train = series[
        series["Month"] < "2025-01-01"
    ]

    history = (
        train["total_demand"]
        .tolist()
    )

    forecasts = []

    for step in range(3):

        temp_df = pd.DataFrame(
            {
                "total_demand": history
            }
        )

        temp_df["Lag_1"] = (
            temp_df["total_demand"]
            .shift(1)
        )

        temp_df["Lag_2"] = (
            temp_df["total_demand"]
            .shift(2)
        )

        temp_df["Lag_3"] = (
            temp_df["total_demand"]
            .shift(3)
        )

        temp_df["Rolling_Mean_3"] = (
            temp_df["total_demand"]
            .rolling(3)
            .mean()
        )

        temp_df = temp_df.dropna()

        X_train = temp_df[
            FEATURE_COLUMNS
        ]

        y_train = temp_df[
            "total_demand"
        ]

        model = LinearRegression()

        model.fit(
            X_train,
            y_train
        )

        next_row = pd.DataFrame(
            {
                "Lag_1": [history[-1]],
                "Lag_2": [history[-2]],
                "Lag_3": [history[-3]],
                "Rolling_Mean_3": [
                    sum(history[-3:]) / 3
                ]
            }
        )

        prediction = (
            model.predict(next_row)[0]
        )

        prediction = max(
            0,
            prediction
        )

        forecasts.append(
            prediction
        )

        history.append(
            prediction
        )

    return forecasts