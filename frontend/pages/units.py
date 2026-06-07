import streamlit as st
import pandas as pd

def units_page():

    st.header("Generating units data")

    df = pd.DataFrame(
        [
            {"Number": i + 1, "Power generation per period": 0}
            for i in range(st.session_state["app"].K)
        ]
    )
    st.data_editor(df)
