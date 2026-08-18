import streamlit as st
from app_state import app

def main_page():
    st.title(app.lang_dict["general_title"])

    st.markdown(app.lang_dict["intro_gms"])

    st.subheader(app.lang_dict["about_app"])
    st.markdown(app.lang_dict["about_text"])

    st.subheader(app.lang_dict["instruction"])
    st.markdown(app.lang_dict["instruction_text"], unsafe_allow_html=True)

    st.subheader(app.lang_dict["sources"])
    st.markdown(app.lang_dict["sources_urls"])