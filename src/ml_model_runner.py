import pandas as pd

from src.ml_forecasting_engine import (
    run_ml_model_for_all_series
)

from src.model_summary import (
    generate_model_summary
)


def run_ml_models(df):

    models = [

        "linear_regression",

        "random_forest",

        "xgboost"

    ]

    comparison_results = []

    for model_name in models:

        print(
            f"\nRunning {model_name}..."
        )

        results_df = (
            run_ml_model_for_all_series(
                df,
                model_name
            )
        )

        results_df.to_excel(
            f"outputs/{model_name}_results.xlsx",
            index=False
        )

        summary = (
            generate_model_summary(
                results_df,
                model_name
            )
        )

        comparison_results.append(
            summary
        )

        print(summary)

    comparison_df = pd.DataFrame(
        comparison_results
    )

    comparison_df.to_excel(
        "outputs/ml_model_comparison.xlsx",
        index=False
    )

    return comparison_df