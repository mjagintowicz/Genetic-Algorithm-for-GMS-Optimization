from units import *

class Individual:
    """
    Individual -- a single schedule
    """
    def __init__(self, schedule):
        self.schedule = schedule
        self.fitness_cost = 0.0
        self.fitness_reliability = 0.0

    def initialize_schedule(self, T, t, K):
        """
        :param T: time horizon
        :param t: number of periods in T
        :param K: number of units
        A schedules will have randomly assigned unit indices (0; K); length T/t
        """
        tmp = []
        self.schedule = tmp

    def calculate_fitness_cost(self, operation_coeff, cf):
        """
        Recalculates fitness of individual. Cost function.
        """
        T = len(self.schedule)
        K = max(self.schedule)
        for k in range(K):  # for each unit analyze the schedules for calcs
            periods_worked = 0
            last_maintenance_period = 0
            for t in range(T):
                k_main = self.schedule[t]       # unit maintained in t
                if k_main == k:                 # if there is maintenance add the working costs and reset, add main cost and remember when it was
                    self.fitness_cost += operation_coeff * periods_worked + cf[t - last_maintenance_period]
                    periods_worked = 0
                    last_maintenance_period = t
                else:   # if there is no maintenance of k, just keep working
                    periods_worked += 1
            self.fitness_cost += operation_coeff * periods_worked   # if there is some unadded work in the end - add it now

    def calculate_fitness_reliability(self, units, demands, t_coeff):

        T = len(self.schedule)
        K = max(self.schedule)
        for t in range(T):
            k_main = self.schedule[t]   # for each t check which k was maintained
            power_generated = 0
            for k in range(K):          # all units except this one worked - sum it's power
                if k != k_main:
                    power_generated += units[k].power * t_coeff
            self.fitness_reliability += power_generated - demands[t]        # check if the demand was exceeded for the t



class Population:
    """
    Population -- a collection of individuals (schedules)
    """

    def __init__(self):
        self.individuals = []

    def initialize_population(self, size, schedules, operation_coeff, cf, units, demands, t_coeff):
        """
        Creates size of random individuals (schedules)
        """
        for i in range(size):
            schedule = Individual(schedules[i])
            schedule.calculate_fitness_cost(operation_coeff, cf)
            schedule.calculate_fitness_reliability(units, demands, t_coeff)
            self.individuals.append(schedule)


class GeneticAlgorithm:

    def __init__(self, population_size, generations, schedules, operation_coeff, cf, units, demands, t_coeff):

        self.population = Population()
        self.population.initialize_population(population_size, schedules, operation_coeff, cf, units, demands, t_coeff)
        self.next_population = []

        self.generations = generations

    def select_parents(self):
        """
        Chooses parents for crossover.
        """
        parent_A = self.population.schedules[0]
        parent_B = self.population.schedules[1]
        return parent_A, parent_B

    def crossover(self, parent_A, parent_B):
        """
        Crossover between parents. Calculate fitness!
        """
        child_A = parent_A
        child_A.calculate_fitness()
        child_B = parent_B
        child_B.calculate_fitness()
        self.next_population.append(child_A)
        self.next_population.append(child_B)

    def mutate(self):
        """
        Mutate an individual (schedule). Either a child or randomly selected. Calculate fitness!
        """
        pass

    def recombine(self):
        """
        After crossover and mutation -- creates a final new population.
        """
        self.population = self.next_population
        self.next_population = []

    def pick_solution(self):
        """
        Chooses the best individual from the population.
        """
        return self.population.schedules[0]


    def run(self):
        """
        Runs the main Genetic Algorithm loop.
        """
        for i in range(self.generations):
            parent_A, parent_B = self.select_parents()
            self.crossover(parent_A, parent_B)
            self.mutate()
            self.recombine()

        return self.pick_solution()
