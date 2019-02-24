from src.backend.utils import *

class Rank(object):
    def __init__(self, req, filter):
        self.request = req
        self.fil = filter
        self.location_dict = {}

    def create_location_dict(self):
        self.fil.filter()
        for city in self.fil.locations:
            self.request.set_travel_city(city)
            hotels = generate_hotel_dict(self.request.get_hotels())
            flights = generate_flight_dict(self.request.get_flight())
            temp_f = flights.items()
            flight_prices =[get_flight_price(offer) for offer, time in temp_f]
            flight_total_times = []
            for i in range(len(temp_f)):
                offer, time = temp_f[i]
                dep, arr = time
                flight_total_times.append(dep+arr)
            price_mean = 0
            for price in flight_prices:
                price_mean += price
            price_mean /= len(flight_prices)

            time_mean = 0
            for time in flight_total_times:
                time_mean += time
            time_mean /= len(flight_total_times)
            min_price = 0
            for i, price in enumerate(flight_prices):
                if price < flight_prices[min_price] and price <= price_mean:
                    if flight_total_times[i] <= time_mean:
                        min_price = i
            best_flight = temp_f[min_price]
            min_price = hotels.values()[0]
            for k,v in hotels.items():
                if v <= min_price:
                    min_price = v
                    best_hotel = k
            self.location_dict[city] = (best_hotel, best_flight)











