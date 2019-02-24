from src.backend.utils import *

class Rank(object):
    def __init__(self, req, filter):
        self.request = req
        self.fil = filter
        self.location_dict = {}

    def create_location_dict(self):
        #self.fil.filter()
        code_dict = {}
        for city in self.fil.locations:
            try:
                self.request.set_travel_city(city)
                code = geocode_city(city)
                if code in code_dict.keys():
                    continue
                code_dict[code] = 1
                hotels = generate_hotel_dict(self.request.get_hotels())
                flights = generate_flight_dict(self.request.get_flight())
                temp_f = list(flights.items())
                flight_prices = [get_flight_price(offer) for offer, time in temp_f]
                flight_total_times = []
                for i in range(len(temp_f)):
                    offer, time = temp_f[i]
                    dep, arr = time
                    flight_total_times.append(dep + arr)
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
                    if float(price) < flight_prices[min_price] and float(price) <= price_mean:
                        if flight_total_times[i] <= time_mean:
                            min_price = i
                best_flight = temp_f[min_price]
                min_price = list(hotels.values())[0]
                for k, v in hotels.items():
                    if v <= min_price:
                        min_price = v
                        best_hotel = (k, v)
                self.location_dict[city] = (best_hotel, best_flight)
            except Exception:
                continue










