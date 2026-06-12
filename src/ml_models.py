from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


FEATURE_COLUMNS = [
    "Lag_1",
    "Lag_2",
    "Lag_3",
    "Rolling_Mean_3"
]


def linear_regression_forecast(
    train,
    test
):

    X_train = train[FEATURE_COLUMNS]
    y_train = train["total_demand"]

    X_test = test[FEATURE_COLUMNS]

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    forecast = model.predict(
        X_test
    )

    return forecast


def random_forest_forecast(
    train,
    test
):

    X_train = train[FEATURE_COLUMNS]
    y_train = train["total_demand"]

    X_test = test[FEATURE_COLUMNS]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    forecast = model.predict(
        X_test
    )

    return forecast


def xgboost_forecast(
    train,
    test
):

    X_train = train[FEATURE_COLUMNS]
    y_train = train["total_demand"]

    X_test = test[FEATURE_COLUMNS]

    model = XGBRegressor(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    forecast = model.predict(
        X_test
    )

    return forecast