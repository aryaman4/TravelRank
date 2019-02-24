from src.backend.utils import *

class Rank(object):
    def __init__(self, req, filter):
        self.request = req
        self.fil = filter
        self.location_dict = {}
        self.indexing = []

    def build_flight_total_time(self, flight_info):
        total_time = []
        for i in range(len(flight_info)):
            offer, info = flight_info[i]
            price, time = info
            dep, arr = time
            total_time.append(dep + arr)
        return total_time


    def create_location_dict(self):
        #self.fil.filter()
        count = 0
        for city in self.fil.locations:
            try:
                print(city)
                print(self.request.current)
                if self.request.generate_city_code(self.request.current) == self.request.generate_city_code(city):
                    continue
                if self.request.generate_city_code(city) in self.location_dict.keys():
                    continue
                self.request.set_travel_city(city)
                try:
                    hotels = generate_hotel_dict(self.request.get_hotels())
                except Exception:
                    continue
                try:
                    flights = generate_flight_dict(self.request.get_flight())
                except Exception:
                    continue
                temp_f = list(flights.items())
                flight_prices = [get_flight_price(offer.offer) for offer, time in temp_f]
                flight_total_times = self.build_flight_total_time(list(temp_f))

                price_mean = 0.0
                for price in flight_prices:
                    price_mean += float(price)
                price_mean /= len(flight_prices)

                time_mean = 0.0
                for time in flight_total_times:
                    time_mean += time
                time_mean /= len(flight_total_times)

                min_price = 0
                for i, price in enumerate(flight_prices):
                    if float(price) < float(flight_prices[min_price]) and float(price) <= price_mean:
                        if flight_total_times[i] <= time_mean:
                            min_price = i
                self.indexing.append(min_price)
                best_flight = temp_f[min_price]
                min_price = list(hotels.values())[0]
                for k, v in hotels.items():
                    if v <= min_price:
                        min_price = v
                        best_hotel = (k, v)
                self.location_dict[self.request.generate_city_code(city)] = (best_hotel, best_flight)

            except Exception:
                continue
            if count == 10:
                break
            count += 1











