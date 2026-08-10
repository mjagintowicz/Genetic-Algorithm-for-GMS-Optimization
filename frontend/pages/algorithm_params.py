import streamlit as st
from app_state import app

criteria = {"COST": "criterion_cost",
            "RELIABILITY":"criterion_reliability"}

selection_ops = {"roulette": "selection_roulette",
                 "tournament": "selection_tournament"}

crossover_ops = ["1-POINT", "2-POINT", "UNIFORM"]

mutation_ops = ["SWAP", "SHIFT"]

def on_param_change(param_kw):
    setattr(app, param_kw, st.session_state[param_kw])

def algorithm_params_page():

    st.title(app.lang_dict["algorithm_params_header"])

    st.subheader(app.lang_dict["population_size"])
    st.number_input(key="population_size", label=app.lang_dict["population_size"], label_visibility="collapsed",
                    min_value=2, max_value=200, value=app.population_size,
                    on_change=on_param_change, args=("population_size",))

    st.subheader(app.lang_dict["generations"])
    st.number_input(key="generations", label=app.lang_dict["generations"], label_visibility="collapsed",
                    min_value=2, max_value=1000, value=app.generations,
                    on_change=on_param_change, args=("generations",))

    st.subheader(app.lang_dict["criterion"])
    st.radio(key="criterion", label=app.lang_dict["criterion"], label_visibility="collapsed",
             options=criteria.keys(), index=list(criteria.keys()).index(app.criterion),
             on_change=on_param_change, args=("criterion",))

    st.subheader(app.lang_dict["selection"])
    st.radio(key="selection_op", label=app.lang_dict["selection"], label_visibility="collapsed",
             options=selection_ops.keys(), index=list(selection_ops.keys()).index(app.selection_op),
            on_change=on_param_change, args=("selection_op",))

    st.subheader(app.lang_dict["selection_rate"])
    st.number_input(key="selection_rate", label=app.lang_dict["selection_rate"], label_visibility="collapsed",
                    min_value=0.01, max_value=1.0, value=app.selection_rate,
                    on_change=on_param_change, args=("selection_rate",))

    st.subheader(app.lang_dict["crossover"])
    st.radio(key="crossover_op", label=app.lang_dict["crossover"], label_visibility="collapsed",
             options=crossover_ops, index=crossover_ops.index(app.crossover_op),
             on_change=on_param_change, args=("crossover_op",))

    st.subheader(app.lang_dict["mutation"])
    st.radio(key="mutation_op", label=app.lang_dict["mutation"], label_visibility="collapsed",
             options=mutation_ops, index=mutation_ops.index(app.mutation_op),
             on_change=on_param_change, args=("mutation_op",))

    st.subheader(app.lang_dict["mutation_rate"])
    st.number_input(key="mutation_rate", label=app.lang_dict["mutation_rate"], label_visibility="collapsed",
                    min_value=0.01, max_value=1.0, value=app.mutation_rate,
                    on_change=on_param_change, args=("mutation_rate",))
    
    st.button(app.lang_dict["run"], key="run", on_click=app.run(), width="stretch", type="primary")