from src.backend.Request import Request
from src.backend.utils import get_formatted_date, get_time, get_price

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
        self.possible_flights = {}
        self.possible_hotels = {}

    def split_budget(self):
        if self.combined is None:
            self.combined = self.factor * self.budget
        travel = 0.6 * self.combined
        lodging = 0.4 * self.combined
        return (travel, lodging)

    def filter_by_travel(self, travel_budget):
        self.request.max_fbudget = travel_budget
        for location in self.locations:
            self.request.travel = location.name
            flight_list = self.request.get_flight()
            possible_flights = list()
            for offer in flight_list:
                price = get_price(offer['offerItems'])
                if price <= travel_budget:
                    possible_flights.append(offer['offerItems'])
            if len(possible_flights) > 0:
                self.possible_flights[location] = possible_flights

    def filter_by_lodging(self, lodging_budget):
        self.request.max_hbudget = lodging_budget
        for location in self.locations:
            self.request.travel = location.name
            hotel_list = self.request.get_hotels()
            possible_hotels = list()

    def filter(self):
        travel, lodging = self.split_budget()
        self.filter_by_travel(travel)
        for location in self.locations:
            if location not in self.possible_flights.keys():
                self.locations.remove(location)
        self.filter_by_lodging(lodging)
