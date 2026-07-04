class Period:
    def __init__(self, demand, unit_maintained):
        self.demand = demand
        self.unit_maintained = unit_maintained

class Unit:

    def __init__(self, power, idx):
        self.power = power
        self.periods_from_last_maintenance = 0
        self.idx = idx

        self.available = True

    def operation_cost(self):
        return self.periods_from_last_maintenance * self.operation_coef

    def is_operation_possible(self):
        return self.available

    def operate(self):
        if not self.available:
            self.available = True
        self.periods_from_last_maintenance += 1

    def maintenance_cost(self, cf):
        return cf[self.periods_from_last_maintenance]

    def is_maintenance_needed(self):
        return not self.available

    def maintain(self):
        if self.available:
            self.available = False
        self.periods_from_last_maintenance = 0


class Schedule:
    def __init__(self):
        self.schedule = []

    def append_unit(self, unit):
        self.schedule.append(unit.idx)