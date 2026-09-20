import streamlit as st
from app_state import app
import pandas as pd

MAX_PERIODS = 104

def load_demands_from_file(uploaded_file):
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)

        if "demand" in df.columns:
            demands = df["demand"].tolist()
        else:
            demands = df.iloc[:, 0].tolist()

    elif uploaded_file.name.lower().endswith(".txt"):
        content = uploaded_file.read().decode("utf-8")

        demands = [float(line.strip().replace(",", ".")) for line in content.splitlines() if line.strip()]

    else:
        st.error(app.lang_dict["wrong_data"])
        return None

    demands = [float(str(demand).replace(",", "."))for demand in demands]

    if len(demands) == 0 or any(demand < 0 for demand in demands):
        st.error(app.lang_dict["wrong_data"])
        return None

    return demands


def load_demands_section():

    uploaded_file = st.file_uploader(app.lang_dict["load_file"], type=["csv", "txt"], key="demands_file",
                                     accept_multiple_files=False, label_visibility="collapsed")

    if uploaded_file is not None:

        if st.button(app.lang_dict["load"], key="load_demands_button"):

            demands = load_demands_from_file(uploaded_file)

            if demands is not None:

                new_T = len(demands)
                app.T = new_T
                st.session_state["T"] = new_T
                st.session_state["demands_values"] = demands
                app.demands = demands

                st.session_state["custom_demand_points"] = [{"period": i + 1,
                                                             "demand": demand}
                                                            for i, demand in enumerate(demands)]

                for t in range(MAX_PERIODS):
                    key = f"demand_{t}"
                    if key in st.session_state:
                        del st.session_state[key]

                st.badge( app.lang_dict["correct_data"], icon=":material/check:", color="green")
                st.rerun()


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
                st.write(f"{app.lang_dict["period"]} {t + 1}")

            with col2:
                st.number_input(app.lang_dict["demand"], min_value=0.0, key=f"demand_{t}")

        submitted = st.form_submit_button(app.lang_dict["save"])

        if submitted:
            demands = [st.session_state[f"demand_{t}"] for t in range(app.T)]
            st.session_state["demands_values"] = demands
            app.demands = demands

            st.badge( app.lang_dict["saved"], icon=":material/check:", color="green")


def on_change_size():

    new_T = st.session_state["T"]
    app.T = new_T

    st.session_state["demands_values"] = [0.0] * new_T
    app.demands = [0.0] * new_T

    for t in range(MAX_PERIODS):
        key = f"demand_{t}"
        if key in st.session_state:
            del st.session_state[key]

def demands_page():

    st.title(app.lang_dict["demands_header"])
    st.warning(app.lang_dict["units_warning"])

    load_demands_section()

    if "T" not in st.session_state:
        st.session_state["T"] = app.T

    st.number_input(key="T", label=app.lang_dict["period_number"], min_value=app.K, max_value=MAX_PERIODS,
                    on_change=on_change_size)

    app.T = st.session_state["T"]

    create_demands_table()