from src.data_preprocessing import (
    load_data
)

from src.recursive_forecasting_engine import (
    run_recursive_linear_regression
)

# Load data
df = load_data(
    "data/final_data_for_vehicle_forecasting.csv"
)

# Run model
results_df = (
    run_recursive_linear_regression(df)
)

# Save output
results_df.to_excel(
    "outputs/recursive_linear_regression_results.xlsx",
    index=False
)

print(results_df.head())

print("\nROWS:")
print(len(results_df))

print("\nAVERAGE MAE")
print(
    round(
        results_df["MAE"].mean(),
        2
    )
)

print("\nAVERAGE MAPE")
print(
    round(
        results_df["MAPE"].mean(),
        2
    )
)

print("\nAVERAGE ACCURACY")
print(
    round(
        results_df["Accuracy"].mean(),
        2
    )
)