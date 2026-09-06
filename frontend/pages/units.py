import streamlit as st
from app_state import app

def create_units_table():
    if "units_power" not in st.session_state:
        st.session_state["units_power"] = [0.0] * app.K

    for k in range(app.K):
        key = f"unit_power_{k}"

        if key not in st.session_state:
            st.session_state[key] = st.session_state["units_power"][k]

    with st.form("units_form"):
        for k in range(app.K):
            col1, col2 = st.columns([1, 3])

            with col1:
                st.write(f"Unit {k + 1}")

            with col2:
                st.number_input("Power [MW]", min_value=0.0, key=f"unit_power_{k}")

        submitted = st.form_submit_button("Save")

        if submitted:
            powers = [st.session_state[f"unit_power_{k}"] for k in range(app.K)]

            st.session_state["units_power"] = powers
            app.assign_units(powers)
            st.badge(app.lang_dict["saved"], icon=":material/check:", color="green")


def on_change_size():
    app.K = st.session_state["K"]

    st.session_state["units_power"] = [0.0] * app.K
    app.units = []

    for k in range(50):
        key = f"unit_power_{k}"

        if key in st.session_state:
            del st.session_state[key]


def units_page():
    st.title(app.lang_dict["units_header"])
    st.caption(app.lang_dict["units_caption"])
    st.warning(app.lang_dict["units_warning"])

    st.number_input(key="K", label=app.lang_dict["units_number"], min_value=1, max_value=50, value=app.K,
                    on_change=on_change_size)

    create_units_table()
