# The main program class (global variables initialization)
# It will run the algorithm

import numpy as np
from backend.charts import Chart
from backend.units import Unit
from backend.ga import GeneticAlgorithm
import streamlit as st


class AppSetup:
    def __init__(self, K, T, cf_1, cf_2, operation_coef, population_size, generations, criterion,
                 selection_op, selection_rate, crossover_op, mutation_op, mutation_rate, lang_dict, elitism, cf):
        self.K = K
        self.T = T
        self.cf_1 = cf_1
        self.cf_2 = cf_2
        self.cf = cf
        self.operation_coef = operation_coef
        self.units = []
        self.demands = []
        self.population_size = population_size
        self.generations = generations
        self.criterion = criterion
        self.selection_op = selection_op
        self.selection_rate = selection_rate
        self.crossover_op = crossover_op
        self.mutation_op = mutation_op
        self.mutation_rate = mutation_rate
        self.lang_dict = lang_dict

        self.elitism = elitism

        self.schedule = []

        self.result = [] # self.best, self.best_abs, self.best_per_gen, self.time, self.generations

    def assign_units(self, power_vec):
        self.units = []
        for k in range(self.K):
            self.units.append(Unit(power_vec[k], k+1))

    def assign_demands(self, demand_vec):
        self.demands = []
        for t in range(self.T):
            self.demands.append(demand_vec[t])

    def maintenance_cost_chart(self):
        chart = Chart(x=range(max(len(self.cf_1), len(self.cf_2))),
                      y=[self.cf_1, self.cf_2],
                      x_label=self.lang_dict["periods_since"],
                      y_label=self.lang_dict["cost"],
                      legend=[r'$cf_1$', r'$cf_2$'])
        return chart.function_plot()

    def operation_cost_chart(self):
        x = np.arange(0, np.size(self.cf_1), 1)
        y = x * self.operation_coef
        chart = Chart(x=x, y=[y],
                      x_label=self.lang_dict["periods_since"],
                      y_label=self.lang_dict["cost"],
                      legend=[self.lang_dict["costs_operation"]])
        return chart.function_plot()

    def schedule_chart(self):
        schedule = self.result[0].schedule

        x = np.arange(0, len(schedule), 1)
        y = schedule

        chart = Chart(x=x, y=[y],
                      x_label=self.lang_dict["period"],
                      y_label=self.lang_dict["unit_num"],)
        return chart.schedule_plot()

    def run(self):
        st.write(self.generations)
        ga = GeneticAlgorithm(population_size=self.population_size,
                              units=self.units,
                              n_periods=self.T,
                              generations=self.generations,
                              operation_coef=self.operation_coef,
                              cf=self.cf,
                              demands=self.demands,
                              criterion=self.criterion,
                              selection_rate=self.selection_rate,
                              selection_op=self.selection_op,
                              crossover_op=self.crossover_op,
                              mutation_rate=self.mutation_rate,
                              mutation_op=self.mutation_op,
                              elitism=self.elitism)
        print("Running...")
        ga.run()
        print("Done!")
        self.result = ga.get_result()

    def convergence_chart(self):
        x = np.arange(0, self.result[4]+1, 1)
        y1 = self.result[1]
        y2 = self.result[2]

        chart = Chart(x=x, y=[y1, y2],
                      x_label=self.lang_dict["generations"],
                      y_label=self.lang_dict["fitness"],
                      legend=[self.lang_dict["best_abs"], self.lang_dict["best_rel"]])
        return chart.function_plot()

