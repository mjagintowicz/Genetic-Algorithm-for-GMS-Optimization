from units import *

class Individual:
    """
    Individual -- a single schedule
    """
    def __init__(self):
        self.schedule = []
        self.fitness = 0.0

    def initialize_schedule(self, T, t, K):
        """
        :param T: time horizon
        :param t: number of periods in T
        :param K: number of units
        A schedules will have randomly assigned unit indices (0; K); length T/t
        """
        tmp = []
        self.schedule = tmp

    def calculate_fitness(self):
        """
        Recalculates fitness of individual. Based on the cost of the schedule and/or nett reserve.
        Basically for each t, gets costs and generation based on the unit order.
        Penalty?
        Maybe use weights as in the article.
        """
        tmp = 1.0
        self.fitness = tmp

class Population:
    """
    Population -- a collection of individuals (schedules)
    """

    def __init__(self):
        self.schedules = []

    def initialize_schedules(self, size, T, t_num, K):
        """
        Creates size of random individuals (schedules)
        """
        for i in range(size):
            schedule = Individual()
            schedule.initialize_schedule(T, t_num, K)
            schedule.calculate_fitness()
            self.schedules.append(schedule)


class GeneticAlgorithm:

    def __init__(self, population_size, T, t_num, K, generations):

        self.population = Population()
        self.population.initialize_schedules(population_size, T, t_num, K)
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
