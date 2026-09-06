import streamlit as st
from app_state import app

def create_demands_table():
    if "demands_values" not in st.session_state:
        st.session_state["demands_values"] = [0.0] * app.T

    for t in range(app.T):
        key = f"demand_{t}"

        if key not in st.session_state:
            st.session_state[key] = st.session_state["demands_values"][t]

    with st.form("demands_form"):
        for t in range(app.T):
            col1, col2 = st.columns([1, 3])

            with col1:
                st.write(f"Period {t + 1}")

            with col2:
                st.number_input("Demand [MW]", min_value=0.0, key=f"demand_{t}")

        submitted = st.form_submit_button("Save")

        if submitted:
            demands = [st.session_state[f"demand_{t}"] for t in range(app.T)]

            st.session_state["demands_values"] = demands
            app.assign_demands(demands)
            st.badge(app.lang_dict["saved"], icon=":material/check:", color="green")

def on_change_size():
    app.T = st.session_state["T"]

    st.session_state["demands_values"] = [0.0] * app.T
    app.demands = []

    for t in range(52):
        key = f"demand_{t}"

        if key in st.session_state:
            del st.session_state[key]

def demands_page():
    st.title(app.lang_dict["demands_header"])

    st.number_input(key="T", label=app.lang_dict["period_number"], min_value=app.K, max_value=52, value=app.T,
                    on_change=on_change_size)

    create_demands_table()