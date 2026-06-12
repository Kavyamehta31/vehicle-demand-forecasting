import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

def evaluate_model(actual, forecast):

    mae = mean_absolute_error(
        actual,
        forecast
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            forecast
        )
    )

    mape = np.mean(
        np.abs(
            (actual - forecast)
            / actual
        )
    ) * 100

    accuracy = 100 - mape

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "Accuracy": accuracy
    }