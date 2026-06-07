import streamlit as st
import pandas as pd

def costs_page():

    st.header("Costs Functions")

    st.subheader("Maintenance")
    st.pyplot(st.session_state["app"].maintenance_cost_chart())