import streamlit as st
import pandas as pd
from app_state import app

def results_page():

    st.header(app.lang_dict["results"])

    if app.result:
        st.subheader(app.lang_dict["schedule"])
        st.session_state["schedule_chart"] = st.pyplot(app.schedule_chart())

        st.subheader(app.lang_dict["objective"])
        st.session_state["convergence_chart"] = st.pyplot(app.convergence_chart())

    else:
        st.info(app.lang_dict["results_missing"])
