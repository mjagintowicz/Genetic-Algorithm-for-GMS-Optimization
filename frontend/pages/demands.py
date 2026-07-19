import streamlit as st
import pandas as pd
from app_state import app

def create_demands_table():
    if "demands" not in st.session_state:
        st.session_state["demands"] = pd.DataFrame(
            [{"Demand per period": 0}
             for _ in range(st.session_state["T"])]
        )

    df = st.data_editor(
        st.session_state["demands"],
        key="demands_editor"
    )

    app.assign_demands(df["Demand per period"].tolist())


def on_change_size():
    app.T = st.session_state["T"]

    st.session_state["demands"] = pd.DataFrame(
        [{"Demand per period": 0}
         for _ in range(app.T)])

    app.demands = []


def demands_page():
    st.header(app.lang_dict["demands_header"])

    st.number_input(key="T", label=app.lang_dict["period_number"],
                    min_value=2, max_value=25, value=app.T,
                    on_change=on_change_size)

    create_demands_table()
