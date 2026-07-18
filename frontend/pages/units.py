import streamlit as st
import pandas as pd
from app_state import app

def create_units_table():
    if "units" not in st.session_state:
        st.session_state["units"] = pd.DataFrame(
            [{"Power generation per period": 0}
             for _ in range(st.session_state["K"])]
        )

    df = st.data_editor(
        st.session_state["units"],
        key="units_editor"
    )
    
    app.assign_units(df["Power generation per period"].tolist())


def on_change_size():
    app.K = st.session_state["K"]

    st.session_state["units"] = pd.DataFrame(
        [{"Power generation per period": 0}
         for _ in range(app.K)])

    app.units = []


def units_page():
    st.header(app.lang_dict["units_header"])
    st.caption(app.lang_dict["units_caption"])
    st.warning(app.lang_dict["units_warning"])

    st.number_input(key="K", label="Number of units",
                    min_value=1, max_value=50, value=app.K,
                    on_change=on_change_size)

    create_units_table()
