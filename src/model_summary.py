def generate_model_summary(
    results_df,
    model_name
):

    summary = {

        "Model": model_name,

        "Average_MAE":
            round(
                results_df["MAE"].mean(),
                2
            ),

        "Average_MAPE":
            round(
                results_df["MAPE"].mean(),
                2
            ),

        "Average_Accuracy":
            round(
                results_df["Accuracy"].mean(),
                2
            ),

        "Series_Count":
            len(results_df)
    }

    return summary