import datetime

class Flight(object):

    def __init__(self, num_people, in_date, out_date, max_budget, time=None):
        self.people = num_people
        self.st_date = in_date
        self.end_date = out_date
        self.max_budget = max_budget
        self.cost = 0
        self.travel_time = time
        
    def check_valid_inputs(self):
        assert self.people is int
        assert self.st_date is datetime
        assert self.end_date is datetime
        assert self.cost is float
        assert self.max_budget is int
        assert self.travel_time is tuple(int, int)
