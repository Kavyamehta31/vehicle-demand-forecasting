import streamlit as st

st.set_page_config(
    page_title="Vehicle Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title(
    "🚚 VECV Vehicle Demand Forecasting System"
)

st.caption(
    "Demand Forecasting • Model Benchmarking • Business Analytics"
)

st.markdown(
    """
    Welcome to the Vehicle Demand Forecasting System.

    Use the navigation menu on the left to explore:

    - Executive Summary
    - Model Comparison
    - Forecast Explorer
    - Download Reports
    """
)

st.info(
    "Select a page from the sidebar."
)