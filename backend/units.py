import random

class Unit:

    def __init__(self, power, idx):
        self.power = power
        self.idx = idx

class Schedule:

    def __init__(self, units, n_periods):

        rng = random.Random()
        self.schedule = [u.idx for u in units]
        self.schedule.extend([0] * (n_periods - len(units)))
        rng.shuffle(self.schedule)