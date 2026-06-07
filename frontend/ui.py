import streamlit as st
import numpy as np
from pages import general, units, costs
from backend.app_setup import AppSetup

if "app" not in st.session_state:
    st.session_state["app"] = AppSetup(20,
                                       25,
                                       np.concatenate((np.full(5, 100),
                                                       np.full(20, 600))),
                                       np.concatenate((np.full(3, 50),
                                                       np.full(7, 150),
                                                       np.full(9, 300),
                                                       np.full(6, 500))),
                                       1, units=None)
pg = st.navigation([
    st.Page(general.main_page, title="Overview"),
    st.Page(units.units_page, title="Units"),
    st.Page(costs.costs_page, title="Costs"),
])

pg.run()