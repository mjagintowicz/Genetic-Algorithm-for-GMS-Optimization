from backend.ga import Population
from backend.ga import GeneticAlgorithm
from debug_db import units, population_size, n_periods, operation_coef, cf, demands, criterion, generations, selection_rate
import unittest

# Check if the population creates correctly +
population = Population(population_size, units, n_periods, operation_coef, cf, demands, criterion)

# Check if the Genetic Algorithm inits correctly +
ga = GeneticAlgorithm(population_size, units, n_periods, operation_coef, cf, demands, criterion, generations, selection_rate)

# Check if the roulette works + creates 12 parents
parents_r = ga.selection_roulette()

# Check if the tournament works + creates 12 parents
parents_t = ga.selection_tournament()

# Check if the repair works
broken_ind = parents_t[0]
print(broken_ind)