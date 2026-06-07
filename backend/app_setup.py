# The main program class (global variables initialization)
# It will run the algorithm

import numpy as np
from backend.charts import Chart


class AppSetup:
    def __init__(self, K, T, cf_1, cf_2, operation_coef, units):
        self.K = K
        self.T = T
        self.cf_1 = cf_1
        self.cf_2 = cf_2
        self.operation_coef = operation_coef
        self.units = units

    def maintenance_cost_chart(self):
        chart = Chart(x=range(max(len(self.cf_1), len(self.cf_2))),
                      y=[self.cf_1, self.cf_2],
                      x_label="Units",
                      y_label="Cost",
                      legend=[r'$cf_1$', r'$cf_2$'])

        return chart.cost_function_plot()

    def run(self):
        # init
        # alg
        pass


app_setup = AppSetup(20,
                     25,
                     np.concatenate((np.full(5, 100),
                                     np.full(20, 600))),
                     np.concatenate((np.full(3, 50),
                                     np.full(7, 150),
                                     np.full(9, 300),
                                     np.full(6, 500))),
                     1, units=None)

#app_setup.run()
