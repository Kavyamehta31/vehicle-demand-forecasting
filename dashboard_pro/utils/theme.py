from pathlib import Path
import streamlit as st


def load_css():

    # Works both locally and on Streamlit Cloud
    css_file = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "style.css"
    )

    if css_file.exists():

        with open(css_file, encoding="utf-8") as f:

            st.markdown(
                f"""
                <style>
                {f.read()}
                </style>
                """,
                unsafe_allow_html=True
            )

    # Hide Streamlit default UI
    st.markdown(
        """
        <style>

        #MainMenu {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        [data-testid="stStatusWidget"] {
            display: none;
        }

        </style>
        """,
        unsafe_allow_html=True
    )