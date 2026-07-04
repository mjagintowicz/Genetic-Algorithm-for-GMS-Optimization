import streamlit as st
import numpy as np
from frontend.pages import general, units, costs

pg = st.navigation([
    st.Page(general.main_page, title="Overview"),
    st.Page(units.units_page, title="Units"),
    st.Page(costs.costs_page, title="Costs"),
])

pg.run()
