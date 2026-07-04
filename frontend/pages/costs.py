import streamlit as st
import pandas as pd
from app_state import app

def on_change_ops():
    app.operation_coef = st.session_state["ops_coef"]

def costs_page():

    st.header("Costs Functions")

    st.subheader("Maintenance cost")
    st.caption("Maintenance costs are described by step functions. Use the default functions or define your own.")
    st.session_state["main_chart"] = st.pyplot(app.maintenance_cost_chart())

    st.subheader("Operation cost")
    st.caption("Operation costs are linear. You can adjust the function coefficient.")

    st.number_input(key="ops_coef", label="Operation cost coefficient",
                    min_value=0.0, max_value=10.0, value=app.operation_coef,
                    on_change=on_change_ops)
    st.session_state["ops_chart"] = st.pyplot(app.operation_cost_chart())
