# The main program class (global variables initialization)
# It will run the algorithm

import numpy as np
from backend.charts import Chart
from backend.units import Unit


class AppSetup:
    def __init__(self, K, T, cf_1, cf_2, operation_coef, population_size, generations, criterion,
                 selection_op, selection_rate, crossover_op, mutation_op, mutation_rate, lang_dict):
        self.K = K
        self.T = T
        self.cf_1 = cf_1
        self.cf_2 = cf_2
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

    def assign_units(self, power_vec):
        self.units = []
        for k in range(self.K):
            self.units.append(Unit(power_vec[k], k+1))

    def assign_demands(self, demand_vec):
        self.demands = []
        for t in range(self.T):
            self.demands.append(Unit(demand_vec[t], t + 1))

    def maintenance_cost_chart(self):
        chart = Chart(x=range(max(len(self.cf_1), len(self.cf_2))),
                      y=[self.cf_1, self.cf_2],
                      x_label="Periods since last maintenance",
                      y_label="Cost",
                      legend=[r'$cf_1$', r'$cf_2$'])
        return chart.cost_function_plot()

    def operation_cost_chart(self):
        x = np.arange(0, np.size(self.cf_1), 1)
        y = x * self.operation_coef
        chart = Chart(x=x, y=[y],
                      x_label="Periods since last maintenance",
                      y_label="Cost",
                      legend=["Operation cost"])
        return chart.cost_function_plot()

    def run(self):
        # init
        # alg
        pass

#app_setup.run()
