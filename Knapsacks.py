class Employee:
    def __init__(self, name, threshold, num_day_off):
        self.name = name
        self.threshold = threshold * 1.
        self.num_day_off = num_day_off
        self.knapsacks = set()

    def add_knapsack(self, obj):
        self.knapsacks.add(obj)
        obj.employee = self

    def __repr__(self):
        return f'name = {self.name}, threshold = {self.threshold}'


