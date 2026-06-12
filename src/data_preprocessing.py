import pandas as pd


def load_data(file_path):

    df = pd.read_csv(file_path)

    df["Month"] = pd.to_datetime(
        df["Month"],
        format="%d/%m/%Y"
    )

    return df


def aggregate_monthly_demand(df):

    monthly_demand = (
        df.groupby("Month")["total_demand"]
          .sum()
          .reset_index()
    )

    return monthly_demand


def train_test_split(monthly_demand):

    train = monthly_demand[
        monthly_demand["Month"] < "2025-01-01"
    ]

    test = monthly_demand[
        monthly_demand["Month"] >= "2025-01-01"
    ]

    return train, test