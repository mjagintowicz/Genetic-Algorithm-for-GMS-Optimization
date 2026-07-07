from backend.ga import GeneticAlgorithm, Individual
from debug_db import units, population_size, n_periods, operation_coef, cf, demands, criterion, generations, selection_rate
import unittest

class TestGAOperators(unittest.TestCase):
    def setUp(self):
        self.ga = GeneticAlgorithm(population_size, units, n_periods, operation_coef, cf, demands, criterion,
                                   generations, selection_rate)

        self.broken_individual_1 = Individual([1, 2, 3, 4, 5, 6, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.broken_individual_2 = Individual([1, 2, 3, 4, 5, 6, 7, 8, 7, 3, 1, 1, 2, 2, 4, 4, 5, 5, 6, 6])

    def test_repair(self):

        # Control input check
        self.assertEqual(len(self.broken_individual_1.schedule), 20)
        self.assertEqual(any(u == 9 for u in self.broken_individual_1.schedule), False)
        self.assertEqual(any(u == 10 for u in self.broken_individual_1.schedule), False)

        self.ga.repair(self.broken_individual_1)
        self.assertEqual(any(u == 9 for u in self.broken_individual_1.schedule), True)
        self.assertEqual(any(u == 10 for u in self.broken_individual_1.schedule), True)

        self.ga.repair(self.broken_individual_2)
        self.assertEqual(any(u == 9 for u in self.broken_individual_2.schedule), True)
        self.assertEqual(any(u == 10 for u in self.broken_individual_2.schedule), True)
        self.assertEqual(any(u == 0 for u in self.broken_individual_2.schedule), False)
        self.assertEqual(any(u == 7 for u in self.broken_individual_2.schedule), True)