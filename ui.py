import streamlit as st
from frontend.pages import general, units, costs, algorithm_params, demands, results
from app_state import app
from frontend.dictionaries import eng, pl

lang_options = {
    "ENG": eng.dict_ENG,
    "PL": pl.dict_PL,
}

def on_lang_change():
    print("BEFORE LANG:", repr(app.selection_op), repr(app.criterion))
    app.lang_dict = lang_options[st.session_state["language"]]
    print("AFTER LANG:", repr(app.selection_op), repr(app.criterion))

st.sidebar.selectbox("", options=lang_options.keys(), key="language", on_change=on_lang_change)

pg = st.navigation([
    st.Page(general.main_page, title=app.lang_dict["general_nav_title"]),
    st.Page(units.units_page, title=app.lang_dict["units_nav_title"]),
    st.Page(demands.demands_page, title=app.lang_dict["demands_nav_title"]),
    st.Page(costs.costs_page, title=app.lang_dict["costs_nav_title"]),
    st.Page(algorithm_params.algorithm_params_page, title=app.lang_dict["algorithm_params_nav_title"]),
    st.Page(results.results_page, title=app.lang_dict["results_nav_title"]),
])

pg.run()
