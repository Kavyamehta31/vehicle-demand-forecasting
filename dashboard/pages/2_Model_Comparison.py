import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Model Comparison",
    layout="wide"
)

st.title("📈 Model Comparison")

# Read comparison file

df = pd.read_excel(
    "outputs/model_comparison.xlsx"
)

st.subheader("Model Performance Table")

st.dataframe(
    df,
    use_container_width=True
)

st.markdown("---")

st.subheader("Average Accuracy by Model")

fig = px.bar(
    df,
    x="Model",
    y="Average_Accuracy",
    text="Average_Accuracy"
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Average MAE by Model")

fig2 = px.bar(
    df,
    x="Model",
    y="Average_MAE",
    text="Average_MAE"
)

fig2.update_layout(
    height=500
)

st.plotly_chart(
    fig2,
    use_container_width=True
)