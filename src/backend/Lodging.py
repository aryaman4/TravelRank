import datetime
class Lodging(object):
    def __init__(self, num_people, st_date, end_date, rating, cost, max_budget):
        self.people = num_people
        self.st_date = st_date
        self.end_date = end_date
        self.rating = rating
        self.cost = cost
        self.max_budget = max_budget

    def check_valid(self):
        assert self.people is int
        assert self.st_date is datetime
        assert self.end_date is datetime
        assert self.rating >= 1
        assert self.cost is float
        assert self.max_budget is int

