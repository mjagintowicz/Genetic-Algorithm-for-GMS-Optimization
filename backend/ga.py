from units import Unit, Schedule
import random

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

    def __init__(self, population_size, units, n_periods, operation_coef, cf, demands, criterion, generations, selection_rate=0.6):

        self.population = Population(population_size, units, n_periods, operation_coef, cf, demands, criterion)
        self.next_population = []

        self.generations = generations
        self.population_size = population_size
        self.selection_rate = selection_rate

        self.best = None

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


    def selection(self, mode):

        # Assume that all are picked for selection

        if mode == "roulette":          # Dispatch the selected mode
            return self.selection_roulette()
        else:
            return self.selection_tournament()


    def crossover(self):
        pass

    def repair(self):
        """
        Repairs new individuals after crossover.
        1. Finds unit indices missing from the schedule.
        2. Replaces random empty period with the maintenance of the missing unit.
        :return:
        """
        pass

    def mutate(self):
        pass

    def recombine(self):
        """
        After crossover and mutation -- creates a final new population.
        """
        self.population = self.next_population
        self.next_population = []

    def run(self):
        """
        Runs the main Genetic Algorithm loop.
        """
        for i in range(self.generations):
            continue

        return self.best
