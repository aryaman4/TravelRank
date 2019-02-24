from amadeus import Client
from src.backend.utils import geocode_city
import pandas as pd

amadeus = Client(
    client_id='ihBJLkd2SDQFIp7MvlHDcAExAFaBiN1n',
    client_secret='XJ2JSLSG0bL5Mky6'
)


class Request(object):


    def __init__(self, current_city = None, travel_city = None, ratings = 'NONE', num_people = '1', st_date = None, end_date = None,max_fbudget = None, max_hbudget = None, currency = 'USD'):
        self.current = current_city
        self.travel = travel_city
        self.ratings = ratings
        self.num_people = num_people
        self.st_date = st_date
        self.end_date = end_date
        self.max_hbudget = max_hbudget
        self.currency = currency
        self.max_fbudget = max_fbudget

    def get_hotels(self):
        lat, long = geocode_city(self.travel)
        request = amadeus.reference_data.locations.airports.get(
            latitude=lat,
            longitude=long
        )
        for i in range(len(request.data)):
            if request.data[i]['address']['cityName'].lower() == self.travel.lower():
                toTravel = request.data[i]['address']['cityCode']
        if (len(self.travel) > 3):
            toTravel = request.data[0]['address']['cityCode']
        request = amadeus.shopping.hotel_offers.get(
            cityCode= toTravel,
            checkInDate = self.st_date,
            checkOutDate = self.end_date,
            currency = self.currency,
            adults = self.num_people,
            ratings= self.ratings or '',
            radius = 50,
            priceRange = self.max_hbudget or ''
        )
        return request.data

    def get_flight(self):
        lat, long = geocode_city(self.current)
        request = amadeus.reference_data.locations.airports.get(
            latitude=lat,
            longitude=long
        )
        for i in range(len(request.data)):
            if request.data[i]['address']['cityName'].lower() == self.current.lower():
                self.current = request.data[i]['address']['cityCode']
        if (len(self.current) > 3):
            self.current = request.data[0]['address']['cityCode']
        lat, long = geocode_city(self.travel)
        request = amadeus.reference_data.locations.airports.get(
            latitude=lat,
            longitude=long
        )
        self.travel = request.data[0]['address']['cityCode']
        request = amadeus.shopping.flight_offers.get(
            origin = self.current,
            destination = self.travel,
            departureDate = self.st_date,
            returnDate = self.end_date or '',
            adults = self.num_people,
            currency = self.currency,
            maxPrice = self.max_fbudget*2
        )
        return request.data

    def get_nearby_airports(self):
        lat, long = geocode_city(self.current)
        request = amadeus.reference_data.locations.airports.get(
            latitude = lat,
            longitude = long
        )
        return [request.data[i]['iataCode'] for i in range(len(request.data))]

    def get_all_cities(self):
        df = pd.read_csv('citylist.csv')
        city = df['name']

        id = df['country_id']

        wanted_cities = [city[i] for i in range(len(city)) if id[i] == 'country:43']

        return wanted_cities

req = Request(current_city='Chicago', travel_city='Knoxville', num_people='2', st_date='2019-04-10', end_date='2019-04-15', ratings='5,4,3,2', max_fbudget=500)

print(req.get_hotels())

print(req.get_flight())
