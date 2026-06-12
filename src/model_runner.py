import pandas as pd

from src.forecasting_engine import (
    run_model_for_all_series
)

from src.model_summary import (
    generate_model_summary
)


def run_statistical_models(df):

    models = [
        "moving_average",
        "ses",
        "holt",
        "arima"
    ]

    comparison_results = []

    for model_name in models:

        print(f"\nRunning {model_name}...")

        results_df = run_model_for_all_series(
            df,
            model_name
        )

        # Save detailed results
        results_df.to_excel(
            f"outputs/{model_name}_results.xlsx",
            index=False
        )

        summary = generate_model_summary(
            results_df,
            model_name
        )

        comparison_results.append(
            summary
        )

        print(summary)

    comparison_df = pd.DataFrame(
        comparison_results
    )

    comparison_df.to_excel(
        "outputs/model_comparison.xlsx",
        index=False
    )

    return comparison_df