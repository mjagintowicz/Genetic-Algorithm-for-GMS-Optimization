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

    st.header(app.lang_dict["algorithm_params_header"])

    st.number_input(key="population_size", label=app.lang_dict["population_size"],
                    min_value=2, max_value=200, value=app.population_size,
                    on_change=on_param_change, args=("population_size",))
    st.number_input(key="generations", label=app.lang_dict["generations"],
                    min_value=2, max_value=1000, value=app.generations,
                    on_change=on_param_change, args=("generations",))

    st.radio(key="criterion", label=app.lang_dict["criterion"], options=criteria.keys(), index=list(criteria.keys()).index(app.criterion),
             on_change=on_param_change, args=("criterion",))

    st.radio(key="selection_op", label=app.lang_dict["selection"], options=selection_ops.keys(), index=list(selection_ops.keys()).index(app.selection_op),
              on_change=on_param_change, args=("selection_op",))

    st.number_input(key="selection_rate", label=app.lang_dict["selection_rate"],
                    min_value=0.01, max_value=1.0, value=app.selection_rate,
                    on_change=on_param_change, args=("selection_rate",))

    st.radio(key="crossover_op", label=app.lang_dict["crossover"], options=crossover_ops,
             index=crossover_ops.index(app.crossover_op),
             on_change=on_param_change, args=("crossover_op",))

    st.radio(key="mutation_op", label=app.lang_dict["mutation"], options=mutation_ops,
             index=mutation_ops.index(app.mutation_op),
             on_change=on_param_change, args=("mutation_op",))

    st.number_input(key="mutation_rate", label=app.lang_dict["mutation_rate"],
                    min_value=0.01, max_value=1.0, value=app.mutation_rate,
                    on_change=on_param_change, args=("mutation_rate",))