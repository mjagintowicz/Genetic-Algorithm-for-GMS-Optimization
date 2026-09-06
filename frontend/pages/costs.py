import streamlit as st
from app_state import app

functions = [r'$cf_1$', r'$cf_2$']

def on_change_ops():
    app.ops_coef = st.session_state["ops_coef"]

def on_param_change(param_kw):
    setattr(app, param_kw, st.session_state[param_kw])

def costs_page():

    st.title(app.lang_dict["costs_header"])

    st.subheader(app.lang_dict["costs_maintenance"])
    st.caption(app.lang_dict["maintenance_caption"])
    st.radio(key="cf", label="", label_visibility="collapsed",
             options=functions,
             on_change=on_param_change, args=("cf",))
    st.session_state["main_chart"] = st.pyplot(app.maintenance_cost_chart())

    st.subheader(app.lang_dict["costs_operation"])
    st.caption(app.lang_dict["operation_caption"])

    st.number_input(key="ops_coef", label=app.lang_dict["operation_coef"],
                    min_value=0.0, max_value=10.0, value=app.ops_coef,
                    on_change=on_param_change, args=("ops_coef",))
    st.session_state["ops_chart"] = st.pyplot(app.operation_cost_chart())
