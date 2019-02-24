import datetime
import requests


def get_formatted_date(date):
    string_date = date.year + "-" + date.month + "-" + date.day
    return string_date


def geocode_city(city_name):
        json = requests.get('https://nominatim.openstreetmap.org/search?q=%s&format=json&polygon=1&addressdetails=1'%(city_name)).json()
        return json[0]['lat'], json[0]['lon']


def get_time(offer):
    departure_seg = offer['offerItems'][0]['services'][0]['segments']
    return_seg = offer['offerItems'][0]['services'][1]['segments']
    departure_time = 0.0
    arrival_time = 0.0
    for segment in departure_seg:
        duration_str = segment['flightSegment']['duration']
        departure_time += convert_to_float(duration_str)
    for segment in return_seg:
        duration_str = segment['flightSegment']['duration']
        arrival_time += convert_to_float(duration_str)
    return departure_time, arrival_time


def generate_flight_dict(flights):
    flight_dict = {}
    offers = [flight for flight in flights]
    prices = [get_flight_price(offer) for offer in flights]
    times = [get_time(offer) for offer in flights]
    for i in range(len(offers)):
        flight_dict[offers[i]] = (prices[i], times[i])
    return flight_dict


def generate_hotel_dict(hotels):
    print(hotels)
    names = [hotels[i]['hotel']['name'] for i in range(len(hotels))]
    totals = [get_hotel_price(offer) for offer in hotels]
    hotel_dict = {}
    for i in range(len(names)):
        hotel_dict[names[i]] = totals[i]
    return hotel_dict


def get_flight_price(offer):
    return offer['offerItems'][0]['pricePerAdult']


def get_hotel_price(offer):
    return offer['offers'][0]['price']['total']

def get_hotel_rating(offer):
    return offer['hotel']['rating']

def convert_to_float(time_str):
    days = int(time_str[0: time_str.find("DT")])
    hours = int(time_str[time_str.find("DT") + 2: time_str.find("H")])
    mins = int(time_str[time_str.find("H") + 1: time_str.find("M")])
    total_hrs = float((days * 24) + (hours) + (mins / 60.0))
    return total_hrs


def convert_to_time_format(time_val):
    mins = int(round((time_val % 1) * 60))
    hrs = int(time_val)
    return hrs, mins
