from statsmodels.tsa.holtwinters import (
    SimpleExpSmoothing,
    Holt,
    ExponentialSmoothing
)

import pandas as pd


def moving_average_forecast(train, periods=3):

    history = list(
        train["total_demand"]
    )

    forecasts = []

    for _ in range(periods):

        forecast = sum(
            history[-3:]
        ) / 3

        forecasts.append(
            forecast
        )

        history.append(
            forecast
        )

    return pd.Series(
        forecasts
    )


def ses_forecast(train, periods=3):

    model = SimpleExpSmoothing(
        train["total_demand"]
    )

    fit_model = model.fit()

    forecast = fit_model.forecast(
        periods
    )

    return forecast


def holt_forecast(train, periods=3):

    model = Holt(
        train["total_demand"]
    )

    fit_model = model.fit()

    forecast = fit_model.forecast(
        periods
    )

    return forecast


def holt_winters_forecast(
    train,
    periods=3
):

    model = ExponentialSmoothing(
        train["total_demand"],
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated"
    )

    fit_model = model.fit()

    forecast = fit_model.forecast(
        periods
    )

    return forecast