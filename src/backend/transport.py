class Transport(object):

    def __init__(self, num_people, in_date, out_date, max_budget, mode=None, time=None):
        self.num = num_people
        self.in_date = in_date
        self.out_date = out_date
        self.max_cost = max_budget
        self.cost = 0
        self.mode = mode
        self.travel_time = time
        
    def check_valid_inputs(self):
        if self.num < 1:
            raise Exception("Number of people is not valid")
