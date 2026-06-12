from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA


def check_stationarity(series):

    result = adfuller(series)

    print("\nADF Statistic:")
    print(result[0])

    print("\np-value:")
    print(result[1])

    if result[1] < 0.05:
        print("\nSeries is Stationary")
    else:
        print("\nSeries is NOT Stationary")


def first_difference(series):

    differenced = series.diff().dropna()

    return differenced


def arima_forecast(train, periods=3):

    model = ARIMA(
        train["total_demand"],
        order=(1, 1, 1)
    )

    fit_model = model.fit()

    forecast = fit_model.forecast(periods)

    return forecast