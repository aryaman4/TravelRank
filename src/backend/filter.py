from src.backend.Request import Request
from src.backend.utils import get_formatted_date, get_flight_price, get_hotel_price, get_hotel_rating

class Filter(object):

    def __init__(self, current_city, num_people, start, end, locations, rating=None, budget=None):
        self.budget = budget
        self.current = current_city
        self.num_people = num_people
        self.start = start
        self.end = end
        self.locations = locations
        self.rating = rating
        self.request = Request(current_city=self.current, num_people=str(num_people), st_date=get_formatted_date(self.start), end_date=get_formatted_date(self.end))
        self.possible_flights = {}
        self.possible_hotels = {}

    def split_budget(self):
        combined = 0.5 * self.budget
        travel = 0.6 * combined
        lodging = 0.4 * combined
        return (travel, lodging)

    def filter_by_travel(self, travel_budget):
        self.request.max_fbudget = travel_budget
        for location in self.locations:
            self.request.set_travel_city(location.name)
            flight_list = self.request.get_flight()
            possible_flights = list()
            for offer in flight_list:
                price = get_flight_price(offer)
                if price <= travel_budget:
                    possible_flights.append(offer)
            if len(possible_flights) > 0:
                self.possible_flights[location] = possible_flights

    def filter_by_lodging(self, lodging_budget):
        self.request.max_hbudget = lodging_budget
        for location in self.locations:
            self.request.set_travel_city(location.name)
            hotel_list = self.request.get_hotels()
            possible_hotels = list()
            for offer in hotel_list:
                price = get_hotel_price(offer)
                rating = get_hotel_rating(offer)
                if price <= lodging_budget and self.rating is not None and int(rating) >= int(self.rating):
                    possible_hotels.append(offer)
            if len(possible_hotels) > 0:
                self.possible_hotels[location] = possible_hotels

    def filter(self):
        travel, lodging = self.split_budget()
        self.request.set_max_hbudget(lodging)
        self.request.set_max_fbudget(travel)
        self.filter_by_travel(travel)
        for location in self.locations:
            if location not in self.possible_flights.keys():
                self.locations.remove(location)
        self.filter_by_lodging(lodging)
        for location in self.locations:
            if location not in self.possible_hotels.keys():
                self.locations.remove(location)
