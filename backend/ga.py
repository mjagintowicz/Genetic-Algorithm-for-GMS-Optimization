from backend.units import Schedule
from collections import Counter
import random
from copy import deepcopy
from time import time, perf_counter

class Individual:
    def __init__(self, schedule_list):
        self.schedule = schedule_list
        self.fitness = 0.0

    def __repr__(self):
        return f"IND: {self.schedule}\nFIT: {self.fitness}\n"

    def calculate_fitness_cost(self, operation_coef, cf, units, demands):
        self.fitness = 0
        T = len(self.schedule)
        K = len(units)

        for k in range(1, K + 1):
            periods_worked = 0

            for t in range(T):
                k_main = self.schedule[t]

                if k_main == k:
                    if periods_worked > 0:
                        self.fitness += cf[periods_worked - 1]
                    elif periods_worked == 0:
                        self.fitness += cf[periods_worked]
                    periods_worked = 0
                else:
                    periods_worked += 1
                    self.fitness += operation_coef * periods_worked

        self.fitness += self.penalty(units, demands)
        self.fitness = 1 / (self.fitness + 1)
        return self.fitness

    def calculate_fitness_reliability(self, units, demands):
        T = len(self.schedule)
        K = len(units)
        reserves = []

        for t in range(T):
            k_main = self.schedule[t]
            power_generated = sum(units[k - 1].power for k in range(1, K + 1) if k != k_main)
            reserves.append(power_generated - demands[t])

        self.fitness = min(reserves)
        return self.fitness

    def nett_reserve(self, units, demands):
        nett_reserve = []

        for t, k_main in enumerate(self.schedule):
            power_generated = 0
            for k in units:
                if k.idx != k_main:
                    power_generated += k.power
            nett_reserve.append(power_generated - demands[t])

        return nett_reserve

    def penalty(self, units, demands):
        nett_reserve = self.nett_reserve(units, demands)
        penalty = 0

        for reserve in nett_reserve:
            if reserve < 0:
                penalty += reserve**2
        return penalty


class Population:
    def __init__(self, size, units, n_periods, operation_coef, cf, demands, criterion):

        self.individuals = []

        for i in range(size):
            schedule = Schedule(units, n_periods)
            individual = Individual(schedule.schedule)
            if criterion == "COST":
                individual.calculate_fitness_cost(operation_coef, cf, units, demands)
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
                 selection_rate=0.6, selection_op="roulette", crossover_op="1_POINT", mutation_rate=0.05, mutation_op="SHIFT",
                 elitism=False):

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
        self.elitism = elitism

        self.best = max(self.population.individuals, key=lambda individual: individual.fitness)
        self.best_abs = [self.best.fitness] # best existing overall individual
        self.best_per_gen = [self.best.fitness] # best individual in each population

        self.time = 0.0

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

        if self.criterion == "COST":
            individual.calculate_fitness_cost(self.operation_coef, self.cf, self.units, self.demands)
        else:
            individual.calculate_fitness_reliability(self.units, self.demands)


    def repair(self, individual):
        """
        Repairs new individuals after crossover.
        1. Finds unit indices missing from the schedule.
        2. Finds free maintenance slots.
        3. If there are not enough slots, a random unit which is maintained > 1 times may free its slot.
        4. Replaces random available slot with the maintenance of the missing unit.
        5. Fixes the consecutive maintenance issue so that the unit can't be maintained for longer than 1 period at once.
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

        # consecutive maintenance fix
        for t in range(1, self.n_periods):

            if individual.schedule[t] != 0 and individual.schedule[t] == individual.schedule[t - 1]:
                unit = individual.schedule[t]
                unit_periods = [i for i, x in enumerate(individual.schedule) if x == unit]
                valid_free_periods = []

                for period in range(self.n_periods):
                    if individual.schedule[period] != 0:
                        continue
                    if all(abs(period - p) >= 2 for p in unit_periods):
                        valid_free_periods.append(period)

                if valid_free_periods:
                    new_period = random.choice(valid_free_periods)
                    individual.schedule[new_period] = unit
                    individual.schedule[t] = 0

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

        if cross_point_1 > cross_point_2:
            cross_point_1, cross_point_2 = cross_point_2, cross_point_1

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

        maintenance_periods = [i for i, x in enumerate(individual.schedule) if x != 0]

        free_periods = [i for i, x in enumerate(individual.schedule) if x == 0]

        if not maintenance_periods or not free_periods:
            return

        idx_1 = random.choice(maintenance_periods)
        idx_2 = random.choice(free_periods)

        unit = individual.schedule[idx_1]

        individual.schedule[idx_1] = 0
        individual.schedule[idx_2] = unit

    def mutation_swap(self, individual):
        maintenance_periods = [i for i, x in enumerate(individual.schedule) if x != 0]

        if len(maintenance_periods) < 2:
            return

        idx_1, idx_2 = random.sample(maintenance_periods, 2)

        individual.schedule[idx_1], individual.schedule[idx_2] = (individual.schedule[idx_2], individual.schedule[idx_1])

    def mutation(self, offspring):
        n_to_mutate = int(self.mutation_rate * len(offspring))

        if n_to_mutate == 0:
            return

        individuals = random.sample(offspring, n_to_mutate)

        for individual in individuals:
            if self.mutation_op == "SHIFT":
                self.mutation_shift(individual)
            else:
                self.mutation_swap(individual)
            self.repair(individual)

    def apply_elitism(self, rate=0.1):
        n_elite = int(rate * len(self.population.individuals))
        elite = sorted(self.population.individuals, key=lambda individual: individual.fitness, reverse=True)[:n_elite]
        return elite

    def replace(self, elite, offspring):
        """
        Replaces the population with elite and offspring. Checks if there's a better solution.
        """
        self.population.individuals = elite + offspring
        best_tmp = max(self.population.individuals, key=lambda individual: individual.fitness)
        if best_tmp.fitness > self.best.fitness:
            self.best = best_tmp
        self.best_abs.append(self.best.fitness)
        self.best_per_gen.append(best_tmp.fitness)

    def prepare_power_series(self):
        power_actual = []

        for idx in self.best.schedule:
            power = 0

            for unit in self.units:
                if unit.idx != idx:
                    power += unit.power

            power_actual.append(power)

        return power_actual

    def get_result(self):
        """
        Function preparing the result individual for display.
        """
        return self.best, self.best_abs, self.best_per_gen, self.time, self.generations, self.prepare_power_series()

    def run(self):
        """
        Runs the main Genetic Algorithm loop.
        """
        start = perf_counter()
        for gen in range(self.generations):
            print("Gen: ", gen)
            elite = deepcopy(self.apply_elitism())
            parents = self.selection()
            target_size = self.population_size - len(elite)
            offspring = deepcopy(self.crossover(parents, target_size))
            self.mutation(offspring)

            self.replace(elite, offspring)
        end = perf_counter()
        self.time = end - start

    def run_cost_for_test(self):
        """
        DEPRECATE
        Prepares formatted data for quicker analysis.
        """
        self.run()
        f_cost = self.best.calculate_fitness_cost(self.operation_coef, self.cf, self.units, self.demands)
        f_cost = (1- f_cost)/f_cost
        self.best.fitness = 0
        f_nett = self.best.calculate_fitness_reliability(self.units, self.demands)
        return f_cost, self.best, self.time, self.prepare_power_series(), f_nett


