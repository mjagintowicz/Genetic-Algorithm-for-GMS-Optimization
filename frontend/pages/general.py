import streamlit as st
from app_state import app

def main_page():
    st.title(app.lang_dict["general_title"])
    st.caption(app.lang_dict["general_caption"])