from backend.units import Unit
import numpy as np

# CREATING INSTANCES FOR TESTING & DEBUGGING

units = [
    Unit(idx=1, power=600),
    Unit(idx=2, power=550),
    Unit(idx=3, power=500),
    Unit(idx=4, power=450),
    Unit(idx=5, power=400),
    Unit(idx=6, power=350),
    Unit(idx=7, power=300),
    Unit(idx=8, power=250),
    Unit(idx=9, power=200),
    Unit(idx=10, power=150),
]

population_size = 20

n_periods = 20

operation_coef = 10
cf = np.concatenate((np.full(5, 100),
                     np.full(20, 600)))

demands = [
    2500, 2550, 2600, 2700, 2800,
    2900, 3000, 3100, 3200, 3300,
    3400, 3300, 3200, 3100, 3000,
    2900, 2800, 2700, 2600, 2500
]

criterion = "Cost"

generations = 10
selection_rate = 0.6

selection_op = "tournament"
crossover_op = "UNIFORM"
mutation_op = "SHIFT"