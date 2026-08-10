import streamlit as st
from app_state import app

def on_change_ops():
    app.operation_coef = st.session_state["ops_coef"]

def costs_page():

    st.header(app.lang_dict["costs_header"])

    st.subheader(app.lang_dict["costs_maintenance"])
    st.caption(app.lang_dict["maintenance_caption"])
    st.session_state["main_chart"] = st.pyplot(app.maintenance_cost_chart())

    st.subheader(app.lang_dict["costs_operation"])
    st.caption(app.lang_dict["operation_caption"])

    st.number_input(key="ops_coef", label=app.lang_dict["operation_coef"],
                    min_value=0.0, max_value=10.0, value=app.operation_coef,
                    on_change=on_change_ops)
    st.session_state["ops_chart"] = st.pyplot(app.operation_cost_chart())
