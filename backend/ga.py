from units import Unit, Schedule
from collections import Counter
import random
from copy import deepcopy

class Individual:
    def __init__(self, schedule_list):
        self.schedule = schedule_list
        self.fitness = 0.0

    def __repr__(self):
        return f"IND: {self.schedule}\nFIT: {self.fitness}"

    def calculate_fitness_cost(self, operation_coef, cf):

        T = len(self.schedule)
        K = max(self.schedule)
        for k in range(K):  # for each unit analyze the schedules for calcs
            periods_worked = 0
            last_maintenance_period = 0
            for t in range(T):
                k_main = self.schedule[t]       # unit maintained in t
                if k_main == k:                 # if there is maintenance add the working costs and reset, add main cost and remember when it was
                    self.fitness += operation_coef * periods_worked + cf[t - last_maintenance_period]
                    periods_worked = 0
                    last_maintenance_period = t
                else:   # if there is no maintenance of k, just keep working
                    periods_worked += 1
            self.fitness += operation_coef * periods_worked   # if there is some unadded work in the end - add it now
            self.fitness = 1 / (self.fitness + 1) # transformed bc it should be minimized

    def calculate_fitness_reliability(self, units, demands):

        T = len(self.schedule)
        K = max(self.schedule)
        for t in range(T):
            k_main = self.schedule[t]   # for each t check which k was maintained
            power_generated = 0
            for k in range(K):          # all units except this one worked - sum it's power
                if k != k_main:
                    power_generated += units[k].power
            self.fitness += power_generated - demands[t]        # check if the demand was exceeded for the t


class Population:
    def __init__(self, size, units, n_periods, operation_coef, cf, demands, criterion):

        self.individuals = []

        for i in range(size):
            schedule = Schedule(units, n_periods)
            individual = Individual(schedule.schedule)
            if criterion == "Cost":
                individual.calculate_fitness_cost(operation_coef, cf)
            else:
                individual.calculate_fitness_reliability(units, demands)
            self.individuals.append(individual)

    def __repr__(self):
        s = ""
        for individual in self.individuals:
            s += f"{individual}\n"
        return s


class GeneticAlgorithm:

    def __init__(self, population_size, units, n_periods, operation_coef, cf, demands, criterion, generations,
                 selection_rate=0.6, selection_op="roulette", crossover_op="1_POINT", mutation_rate=0.05, mutation_op="SHIFT"):

        self.population = Population(population_size, units, n_periods, operation_coef, cf, demands, criterion)
        self.next_population = []

        self.generations = generations
        self.population_size = population_size
        self.selection_rate = selection_rate
        self.units = units
        self.n_periods = n_periods
        self.operation_coef = operation_coef
        self.cf = cf
        self.demands = demands
        self.criterion = criterion
        self.crossover_op = crossover_op
        self.mutation_rate = mutation_rate
        self.mutation_op = mutation_op
        self.selection_op = selection_op

        self.best = max(self.population.individuals, key=lambda individual: individual.fitness)

    def selection_roulette(self):

        individuals = self.population.individuals
        total_fitness = sum(ind.fitness for ind in individuals)

        parents = []
        n_parents = int(self.selection_rate * self.population_size)
        for n in range(n_parents):

            r = random.uniform(0, total_fitness)
            current_sum = 0

            for ind in individuals:
                current_sum += ind.fitness

                if current_sum >= r:
                    parents.append(ind)
                    break
        return parents


    def selection_tournament(self, tournament_size=3):
        parents = []
        individuals = self.population.individuals

        n_parents = int(self.selection_rate * self.population_size)
        for i in range(n_parents):
            tournament = random.sample(individuals, tournament_size)
            winner = max(tournament, key=lambda ind: ind.fitness)
            parents.append(winner)

        return parents


    def selection(self):

        if self.selection_op == "roulette":
            parents = self.selection_roulette()
        else:
            parents = self.selection_tournament()

        if len(parents) % 2 == 1:
            parents.pop()

        random.shuffle(parents)
        return parents


    def adjust_fitness(self, individual):

        if self.criterion == "Cost":
            individual.calculate_fitness_cost(self.operation_coef, self.cf)
        else:
            individual.calculate_fitness_reliability(self.units, self.demands)


    def repair(self, individual):
        """
        Repairs new individuals after crossover.
        1. Finds unit indices missing from the schedule.
        2. Finds free maintenance slots.
        3. If there are not enough slots, a random unit which is maintained > 1 times may free its slot.
        4. Replaces random available slot with the maintenance of the missing unit.
        5. Recalculates fitness.
        """
        counts = Counter(individual.schedule)
        missing_units = [u.idx for u in self.units if counts[u.idx] == 0]
        free_periods = [t for t, u in enumerate(individual.schedule) if u == 0]

        if len(missing_units) > len(free_periods):
            seen = Counter()
            duplicates = []
            for t, u in enumerate(individual.schedule):
                if u != 0:
                    seen[u] += 1
                if seen[u] > 1:
                    duplicates.append(t)

            free_periods += list(set(duplicates))

        random.shuffle(missing_units)
        random.shuffle(free_periods)

        for (u, t) in zip(missing_units, free_periods):
            individual.schedule[t] = u

        self.adjust_fitness(individual)


    def crossover_1_point(self, parent1, parent2):

        cross_point = random.randint(0, self.n_periods - 1)
        new_schedule_1 = parent1.schedule[:cross_point] + parent2.schedule[cross_point:]
        new_schedule_2 = parent2.schedule[:cross_point] + parent1.schedule[cross_point:]

        return new_schedule_1, new_schedule_2


    def crossover_2_point(self, parent1, parent2):

        cross_point_1 = random.randint(0, self.n_periods - 1)
        cross_point_2 = cross_point_1

        while cross_point_1 == cross_point_2:
            cross_point_2 = random.randint(0, self.n_periods - 1)

        new_schedule_1 = parent1.schedule[:cross_point_1] + parent2.schedule[cross_point_1:cross_point_2] + parent1.schedule[cross_point_2:]
        new_schedule_2 = parent2.schedule[:cross_point_1] + parent1.schedule[cross_point_1:cross_point_2] + parent2.schedule[cross_point_2:]

        return new_schedule_1, new_schedule_2


    def crossover_uniform(self, parent_1, parent_2):

        new_schedule_1 = []
        new_schedule_2 = []

        for t in range(self.n_periods):
            rng = random.uniform(0, 1)
            if rng < 0.5:
                new_schedule_1.append(parent_1.schedule[t])
                new_schedule_2.append(parent_2.schedule[t])
            else:
                new_schedule_1.append(parent_2.schedule[t])
                new_schedule_2.append(parent_1.schedule[t])

        return new_schedule_1, new_schedule_2


    def crossover(self, parents, target_size):
        """
        The main crossover function.
        1. Creates new schedules using the picked operator.
        2. Turns the schedules into the individuals.
        3. Repairs.
        """

        offspring = []

        while len(offspring) < target_size:
            parent_1, parent_2 = random.sample(parents, 2)

            if self.crossover_op == "1_POINT":
                new_schedule_1, new_schedule_2 = self.crossover_1_point(parent_1, parent_2)
            elif self.crossover_op == "2_POINT":
                new_schedule_1, new_schedule_2 = self.crossover_2_point(parent_1, parent_2)
            else:
                new_schedule_1, new_schedule_2 = self.crossover_uniform(parent_1, parent_2)

            individual_1 = Individual(new_schedule_1)
            individual_2 = Individual(new_schedule_2)

            self.repair(individual_1)
            self.repair(individual_2)

            offspring.append(individual_1)
            offspring.append(individual_2)

        return offspring[:target_size]

    def mutation_shift(self, individual):
        """
        1. Selects a maintenance to shift.
        2. Moves it to a different free slot.
        """

        while True:
            idx_1 = random.randint(0, self.n_periods - 1)
            unit = individual.schedule[idx_1]
            if unit != 0:
                break

        free_periods = [i for i, x in enumerate(individual.schedule) if x == 0]
        idx_2 = random.choice(free_periods)

        individual.schedule[idx_1] = 0
        individual.schedule[idx_2] = unit

    def mutation_swap(self, individual):
        """
        1. Selects two maintenances.
        2. Swaps their places.
        """
        while True:
            idx_1 = random.randint(0, self.n_periods - 1)
            unit_1 = individual.schedule[idx_1]
            if unit_1 != 0:
                break
        while True:
            idx_2 = random.randint(0, self.n_periods - 1)
            unit_2 = individual.schedule[idx_2]
            if unit_2 != 0 and idx_1 != idx_2:
                break

        individual.schedule[idx_1] = unit_2
        individual.schedule[idx_2] = unit_1


    def mutation(self, offspring):

        n_to_mutate = int(self.mutation_rate * len(offspring))
        individuals = random.sample(offspring, n_to_mutate)
        for individual in individuals:
            if self.mutation_op == "SHIFT":
                self.mutation_shift(individual)
            else:
                self.mutation_swap(individual)

    def elitism(self, rate=0.1):
        n_elite = int(rate * len(self.population.individuals))
        elite = sorted(self.population.individuals,key=lambda individual: individual.fitness)[:n_elite]
        return elite

    def replace(self, elite, offspring):
        """
        Replaces the population with elite and offspring. Checks if there's a better solution.
        """
        self.population.individuals = elite + offspring
        best_tmp = max(self.population.individuals, key=lambda individual: individual.fitness)
        if best_tmp.fitness > self.best.fitness:
            self.best = best_tmp

    def run(self):
        """
        Runs the main Genetic Algorithm loop.
        """
        for gen in range(self.generations):
            elite = deepcopy(self.elitism())
            parents = self.selection()
            target_size = self.population_size - len(elite)
            offspring = deepcopy(self.crossover(parents, target_size))
            self.mutation(offspring)

            self.replace(elite, offspring)

        return self.best
