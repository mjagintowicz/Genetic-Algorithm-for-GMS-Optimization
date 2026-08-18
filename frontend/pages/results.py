import streamlit as st
import pandas as pd
from app_state import app

def results_page():

    st.header(app.lang_dict["results"])

    st.session_state["schedule_chart"] = st.pyplot(app.schedule_chart())
    st.session_state["convergence_chart"] = st.pyplot(app.convergence_chart())