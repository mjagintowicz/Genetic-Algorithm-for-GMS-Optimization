import streamlit as st
import pandas as pd
from app_state import app

def results_page():

    st.session_state["res_chart"] = st.pyplot(app.schedule_chart())