from amadeus import Client, ResponseError
from src.backend.utils import geocode_city
import pandas as pd
import requests

API_KEY = 'ihBJLkd2SDQFIp7MvlHDcAExAFaBiN1n' #replace for use
API_SECRET = 'XJ2JSLSG0bL5Mky6'
amadeus = Client(
    client_id=API_KEY,
    client_secret=API_SECRET
)


class Request(object):
    def __init__(self, current_city=None, travel_city=None, ratings='NONE',
                 num_people='1', st_date=None, end_date=None, max_fbudget=None, max_hbudget=None, currency='USD'):
        self.current = current_city
        self.travel = travel_city
        self.ratings = ratings
        self.num_people = num_people
        self.st_date = st_date
        self.end_date = end_date
        self.max_hbudget = max_hbudget
        self.currency = currency
        self.max_fbudget = max_fbudget

    def set_travel_city(self, city):
        self.travel = city

    def set_max_fbudget(self, fbudget):
        self.max_fbudget = fbudget

    def set_max_hbudget(self, hbudget):
        self.max_hbudget = hbudget

    @staticmethod
    def generate_city_code(name):
        with open('citycodes.csv') as file:
            lines = file.readlines()
        codes = []
        for line in lines:
            if name in line:
                codes.append(line[len(line) - 4:].strip())
        return codes

    def get_hotels(self):
        lat, longi = geocode_city(self.travel)
        request = amadeus.reference_data.locations.airports.get(
            latitude=lat,
            longitude=longi
        )
        toTravel = ""
        print(self.travel)
        for i in range(len(request.data)):
            if request.data[i]['address']['cityName'].lower() == self.travel.lower():
                toTravel = request.data[i]['address']['cityCode']
        if toTravel == '' and len(request.data) != 0:
            toTravel = request.data[0]['address']['cityCode']
        request = amadeus.shopping.hotel_offers.get(
            cityCode=toTravel,
            checkInDate=self.st_date,
            checkOutDate=self.end_date,
            currency=self.currency,
            adults=self.num_people
        )
        return request.data

    def get_flight(self):
        curr_city = Request.generate_city_code(self.current)
        travel_city = Request.generate_city_code(self.travel)
        responses = []
        for i in range(len(curr_city)):
            for j in range(len(travel_city)):
                response = requests.get(
                    "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/%s/%s/%s?inboundpartialdate=%s" % (
                    curr_city[i], travel_city[j], self.st_date, self.end_date),
                    headers={
                        "X-RapidAPI-Key": "bb86748db8msh78323291d276d73p187f9djsn020b5eb40155"
                    }
                )
                if int(response.status_code) == 200:
                    responses.append((response.json(),response.json()['Quotes'][0]['MinPrice']))
        minimum = self.max_fbudget
        for r in responses:
            js, price = r
            if int(price) < minimum:
                flight_json = js
                minimum = price
        return flight_json


    @staticmethod
    def get_all_cities():
        df = pd.read_csv('citylist.csv')
        city = df['name']
        id = df['country_id']
        wanted_cities = [city[i] for i in range(len(city)) if id[i] == 'country:43']
        return wanted_cities

import time
start = time.time()
r = Request("Chicago", "San Francisco", st_date='2019-05-03', end_date='2019-05-09', max_fbudget=200)
print(r.get_flight())
end = time.time()
print(end - start)
