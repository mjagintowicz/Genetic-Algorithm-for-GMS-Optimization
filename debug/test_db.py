from backend.units import Unit
import numpy as np
from backend.ga import GeneticAlgorithm

U = 21
units = [
    Unit(idx=1,  power=555),
    Unit(idx=2,  power=180),
    Unit(idx=3,  power=180),
    Unit(idx=4,  power=640),
    Unit(idx=5,  power=640),
    Unit(idx=6,  power=276),
    Unit(idx=7,  power=140),
    Unit(idx=8,  power=90),
    Unit(idx=9,  power=76),
    Unit(idx=10, power=94),
    Unit(idx=11, power=39),
    Unit(idx=12, power=188),
    Unit(idx=13, power=52),
    Unit(idx=14, power=555),
    Unit(idx=15, power=640),
    Unit(idx=16, power=555),
    Unit(idx=17, power=76),
    Unit(idx=18, power=58),
    Unit(idx=19, power=48),
    Unit(idx=20, power=137),
    Unit(idx=21, power=469),
]

# Yearly demand with higher demand in the beginning
T = 52
demands = [
    4739, 4310, 4080, 4029, 3952, 3927, 3875, 3824,
    3773, 3748, 3722, 3697, 3651, 3645, 3594, 3569,
    3543, 3518, 3492, 3467, 3416, 3390, 3339, 3313,
    3262, 3211, 3160, 3109, 3058, 3007, 2981, 2930,
    2854, 2802, 2726, 2675, 2598, 2521, 2470, 2419,
    2394, 2317, 2291, 2266, 2240, 2215, 2164, 2138,
    2087, 2010, 1755, 1500
]

# Maintenance costs for calculations (chart/display form can stay the same)
def maintenance_cost_1(periods):
    if periods <= 5:
        return 100
    return 600

def maintenance_cost_2(periods):
    if periods <= 3:
        return 50
    elif periods <= 10:
        return 150
    elif periods <= 19:
        return 300
    return 500

# GA experiment parameters
population_size = 100 # [50 100 200]
generations = 10  # [100, 500, 1000, 2000, 5000]
selection_rate = 0.6 # [0.4, 0.6, 0.8, 1]
mutation_rate = 0.05 # [0.01 0.05 0.1 0.2]

# GA comparison parameters -- compare results for all options
criterion = "COST"
selection_op = "roulette"
crossover_op = "1-POINT"
mutation_op = "SHIFT"

cf=np.concatenate((np.full(3, 50),
                np.full(7, 150),
                np.full(9, 300),
                np.full(6, 500),
                np.full(27, 500)))


# ~30 runs for each experiment
ga = GeneticAlgorithm(population_size, units, T, 10, cf, demands, criterion, generations,
                      selection_rate=selection_rate, selection_op=selection_op, crossover_op=crossover_op,
                      mutation_op=mutation_op, elitism=False)
print(ga.run())
