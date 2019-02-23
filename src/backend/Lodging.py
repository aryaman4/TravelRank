import datetime
import json
from src.backend.Request import Request


class Lodging(object):
    def __init__(self,travel_city, num_people, st_date, end_date, rating, cost, max_budget, request):
        self.people = num_people
        self.st_date = st_date
        self.end_date = end_date
        self.rating = rating
        self.cost = cost
        self.max_budget = max_budget
        self.travel = travel_city
        self.request = Request(travel_city=travel_city, ratings=rating, num_people=num_people, st_date=st_date, end_date=end_date, max_hbudget=max_budget)

    def check_valid(self):
        assert self.people is int
        assert self.st_date is datetime
        assert self.end_date is datetime
        assert self.rating >= 1
        assert self.cost is float
        assert self.max_budget is int

    def get_name_price(self):
        hotels = self.request.get_hotels()
        names = [hotels[i]['name'] for i in range(len(hotels))]
        totals = [hotels[i]['offers'][0]['price']['total'] for i in range(len(hotels))]
        hotel_dict = {}
        for i in range(len(names)):
            hotel_dict[hotels[i]] = totals[i]
        return hotel_dict


