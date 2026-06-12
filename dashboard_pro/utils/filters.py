import streamlit as st


def create_filters(df):

    st.sidebar.header("Filters")

    # HALB Filter
    halb = st.sidebar.selectbox(
        "HALB",
        ["All"] + sorted(
            df["Halb"]
            .astype(str)
            .dropna()
            .unique()
            .tolist()
        )
    )

    # Engine Filter
    engine = st.sidebar.selectbox(
        "Engine",
        ["All"] + sorted(
            df["engine_type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    # Model Filter
    model = st.sidebar.selectbox(
        "Model",
        ["All"] + sorted(
            df["map_model"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    # Vehicle Type Filter
    vehicle = st.sidebar.selectbox(
        "Vehicle Type",
        ["All"] + sorted(
            df["Vehicle_Type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    return halb, engine, model, vehicle