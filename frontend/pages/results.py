import streamlit as st
from app_state import app

def results_page():

    st.title(app.lang_dict["results"])

    if app.result:

        cost, reliability = app.prepare_result_values()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(label=app.lang_dict["criterion_cost"], value=f"{cost:.2f}")

        with col2:
            st.metric(label=app.lang_dict["criterion_reliability"], value=f"{reliability:.2f}")

        st.subheader(app.lang_dict["schedule"])
        st.session_state["schedule_chart"] = st.pyplot(app.schedule_chart())

        st.subheader(app.lang_dict["power_gen"])
        st.session_state["power_gen_chart"] = st.pyplot(app.power_gen_chart())

        st.subheader(app.lang_dict["objective"])
        st.session_state["convergence_chart"] = st.pyplot(app.convergence_chart())

    else:
        st.info(app.lang_dict["results_missing"])
