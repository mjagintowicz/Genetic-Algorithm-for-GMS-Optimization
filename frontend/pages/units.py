import streamlit as st
from app_state import app
import pandas as pd

MAX_UNITS = 100

def load_units_from_file(uploaded_file):
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)

        if "power" in df.columns:
            powers = df["power"].tolist()
        else:
            powers = df.iloc[:, 0].tolist()

    elif uploaded_file.name.lower().endswith(".txt"):
        content = uploaded_file.read().decode("utf-8")
        powers = [float(line.strip())for line in content.splitlines() if line.strip()]

    else:
        st.error(app.lang_dict["wrong_data"])
        return None

    powers = [float(power) for power in powers]

    if len(powers) == 0 or any(power < 0 for power in powers):
        st.error(app.lang_dict["wrong_data"])
        return None

    return powers


def load_units_section():

    uploaded_file = st.file_uploader(app.lang_dict["load_file"], type=["csv", "txt"], key="units_file",
                                     accept_multiple_files=False, label_visibility="collapsed")

    if uploaded_file is not None:

        if st.button(app.lang_dict["load"], key="load_units_button"):
            powers = load_units_from_file(uploaded_file)

            if powers is not None:

                new_K = len(powers)
                app.K = new_K
                st.session_state["K"] = new_K
                st.session_state["units_power"] = powers

                for k in range(MAX_UNITS):
                    key = f"unit_power_{k}"
                    if key in st.session_state:
                        del st.session_state[key]

                app.assign_units(powers)
                st.badge( app.lang_dict["correct_data"], icon=":material/check:", color="green")
                st.rerun()


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
                st.write(f"{app.lang_dict["unit"]} {k + 1}")

            with col2:
                st.number_input(app.lang_dict["power_label"], min_value=0.0, key=f"unit_power_{k}")

        submitted = st.form_submit_button(app.lang_dict["save"])

        if submitted:
            powers = [st.session_state[f"unit_power_{k}"] for k in range(app.K)]

            st.session_state["units_power"] = powers

            app.assign_units(powers)

            st.badge( app.lang_dict["saved"], icon=":material/check:", color="green")


def on_change_size():

    new_K = st.session_state["K"]
    app.K = new_K
    st.session_state["units_power"] = [0.0] * new_K
    app.units = []

    for k in range(MAX_UNITS):
        key = f"unit_power_{k}"
        if key in st.session_state:
            del st.session_state[key]


def units_page():

    st.title(app.lang_dict["units_header"])
    st.caption(app.lang_dict["units_caption"])
    st.warning(app.lang_dict["units_warning"])

    load_units_section()

    if "K" not in st.session_state:
        st.session_state["K"] = app.K

    st.number_input(key="K", label=app.lang_dict["units_number"], min_value=1, max_value=100, on_change=on_change_size)

    app.K = st.session_state["K"]

    create_units_table()