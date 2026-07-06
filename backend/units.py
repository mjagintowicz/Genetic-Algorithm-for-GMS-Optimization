import random

class Period:
    def __init__(self, demand, unit_maintained):
        self.demand = demand
        self.unit_maintained = unit_maintained

class Unit:

    def __init__(self, power, idx):
        self.power = power
        self.idx = idx

        self.available = True

    def is_operation_possible(self):
        return self.available

    def is_maintenance_needed(self):
        return not self.available


class Schedule:

    def __init__(self, units, n_periods):

        rng = random.Random()
        self.schedule = [u.idx for u in units]
        self.schedule.extend([0] * (n_periods - len(units)))
        rng.shuffle(self.schedule)