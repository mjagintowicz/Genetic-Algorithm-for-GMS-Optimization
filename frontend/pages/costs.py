import streamlit as st
from app_state import app

functions = [r'$cf_1$', r'$cf_2$', 'Other']

def build_custom_cf(periods, costs, T):
    cf = [0.0] * T

    points = sorted(zip(periods, costs), key=lambda x: x[0])

    for i, (period, cost) in enumerate(points):
        start = 0 if i == 0 else points[i - 1][0]
        end = period

        for t in range(start, end):
            cf[t] = cost

    last_period, last_cost = points[-1]

    for t in range(last_period, T):
        cf[t] = last_cost

    return cf


def custom_cost_function():
    if "custom_cf_points" not in st.session_state:
        st.session_state["custom_cf_points"] = [{"period": 1, "cost": 0.0}]

    points = st.session_state["custom_cf_points"]

    with st.form("custom_cf_form"):
        new_points = []

        for i, point in enumerate(points):
            col1, col2 = st.columns([1, 2])

            with col1:
                period = st.number_input(app.lang_dict["period"], min_value=1, max_value=app.T,
                                         value=min(point["period"], app.T), key=f"custom_period_{i}")

            with col2:
                cost = st.number_input(app.lang_dict["cost"], min_value=0.0, value=point["cost"],
                                       key=f"custom_cost_{i}")

            new_points.append({"period": period, "cost": cost})

        submitted = st.form_submit_button("Save")

    if submitted:
        periods = [point["period"] for point in new_points]
        costs = [point["cost"] for point in new_points]

        if any(periods[i] >= periods[i + 1] for i in range(len(periods) - 1)):
            st.error(app.lang_dict["period_error"])
            return

        st.session_state["custom_cf_points"] = new_points
        app.cf_other = build_custom_cf(periods, costs, app.T)

        if st.session_state["cf"] == "Other":
            app.cf = app.cf_other

        st.badge( app.lang_dict["saved"], icon=":material/check:", color="green")

    if len(points) < app.T:
        if st.button(app.lang_dict["add_period"], key="add_custom_period"):
            last_period = points[-1]["period"]

            next_period = min(last_period + 1, app.T)

            if next_period > last_period:
                points.append({"period": next_period,
                               "cost": points[-1]["cost"]})
                st.rerun()


def on_change_cf():
    selected = st.session_state["cf"]

    if selected == r'$cf_1$':
        app.cf = app.cf_1

    elif selected == r'$cf_2$':
        app.cf = app.cf_2

    elif selected == "Other":
        app.cf = app.cf_other


def on_param_change(param_kw):
    setattr(app, param_kw, st.session_state[param_kw])

def costs_page():

    st.title(app.lang_dict["costs_header"])

    st.subheader(app.lang_dict["costs_maintenance"])
    st.caption(app.lang_dict["maintenance_caption"])

    if "cf" not in st.session_state:
        st.session_state["cf"] = r'$cf_1$'

    st.radio(key="cf", label="", label_visibility="collapsed", options=functions, on_change=on_change_cf )
    selected = st.session_state["cf"]

    if selected == r'$cf_1$':
        app.cf = app.cf_1

    elif selected == r'$cf_2$':
        app.cf = app.cf_2

    elif selected == "Other":
        app.cf = app.cf_other
        custom_cost_function()

    st.session_state["main_chart"] = st.pyplot(app.maintenance_cost_chart())

    st.subheader(app.lang_dict["costs_operation"])
    st.caption(app.lang_dict["operation_caption"])

    st.number_input(key="ops_coef", label=app.lang_dict["operation_coef"],
                    min_value=0.0, max_value=10.0, value=app.ops_coef,
                    on_change=on_param_change, args=("ops_coef",))

    st.session_state["ops_chart"] = st.pyplot(app.operation_cost_chart())

    st.subheader(app.lang_dict["penalty"])
    st.number_input(key="penalty_coef", label=app.lang_dict["penalty"], label_visibility="collapsed",
                    min_value=0, max_value=1000, value=app.penalty_coef, on_change=on_param_change,
                    args=("penalty_coef",))
