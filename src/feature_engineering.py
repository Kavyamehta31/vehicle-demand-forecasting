import pandas as pd


def create_time_series_features(monthly_demand):

    df = monthly_demand.copy()

    df["Lag_1"] = df["total_demand"].shift(1)
    df["Lag_2"] = df["total_demand"].shift(2)
    df["Lag_3"] = df["total_demand"].shift(3)

    df["Rolling_Mean_3"] = (
        df["total_demand"]
        .rolling(window=3)
        .mean()
    )

    df = df.dropna()

    return df