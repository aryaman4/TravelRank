from src.backend.Request import Request
from src.backend.utils import get_formatted_date

class Filter(object):

    def __init__(self, current_city, num_people, start, end, locations, mode=None, time=None, rating=None, budget=None, travel_lodging=None):
        self.budget = budget
        self.current = current_city
        self.num_people = num_people
        self.start = start
        self.end = end
        self.locations = locations 
        self.combined = travel_lodging
        self.enough = True
        self.factor = 0.5
        self.request = Request(current_city=self.current, num_people=str(num_people), st_date=get_formatted_date(self.start), end_date=get_formatted_date(self.end))

    def split_budget(self):
        if self.combined is None:
            self.combined = self.factor * self.budget
        travel = 0.6 * self.combined
        lodging = 0.4 * self.combined
        return (travel, lodging)

    def filter_by_travel(self, travel_budget):
        self.request.fbudget = travel_budget
        for location in self.locations:
            self.request.travel = location.name
            flight_list = self.request.get_flight()
            for offer in flight_list:
                departure_time, arrival_time = get_time(offer)
                price_per_adult = get_price(offer)

    def filter_by_lodging(self, lodging_budget):
        pass

    def filter(self):
        travel, lodging = self.split_budget()
        self.filter_by_travel(travel)
        self.filter_by_lodging(lodging)
