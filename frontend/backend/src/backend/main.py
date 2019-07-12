from src.backend.filter import Filter
from src.backend.Request import Request
from src.backend.Rank import Rank
from src.backend.utils import generate_hotel_dict, generate_flight_dict, sort_y_pred
from src.backend.regression import predict_rank
import random

class Main(object):

    def __init__(self, budget, current_city, start_date, end_date, num_people, hotel_rating = None):
        self.budget = budget
        self.current = current_city
        self.st_date = start_date
        self.end_date = end_date
        self.people = num_people
        self.rating = hotel_rating
        self.fil = Filter(current_city=self.current, rating=self.rating, num_people=self.people, budget=self.budget, start=start_date, end=end_date, locations=None)

    def get_output_list_ranked(self):
        city_list = Request.get_all_cities()
        city_list = city_list[:10]
        self.fil.locations = city_list
        ranker = Rank(self.fil.request, self.fil)
        ranker.create_location_dict()
        x_vals = list()
        for city, val in ranker.location_dict.items():
            hotel, flight = val
            hotel_dict = generate_flight_dict(self.fil.request.get_hotels())
            flight_dict = generate_flight_dict(self.fil.request.get_flight())
            hotel_price = hotel_dict[hotel]
            flight_price = flight_dict[flight][0]
            flight_time = flight_dict[flight][1][0] + flight_dict[flight][1][1]
            x_vals.append([city, hotel_price, flight_price, flight_time])
        y_pred = predict_rank(x_vals[1:])
        x_pred, y_pred = sort_y_pred(x_vals, y_pred)
        return x_pred

    def get_other_ten(self, city_list):
        item_list = list()
        item = None
        for i in range(10):
            random.choice(city_list)

    def return_json(self):
        x_pred = self.get_output_list_ranked()
        location_list = list()
        for pred in x_pred:
            name = pred[0]
