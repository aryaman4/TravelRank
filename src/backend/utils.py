import datetime
import requests
def get_formatted_date(date):
        string_date = date.year + "-" + date.month + "-" + date.day
        return string_date

def geocode_city(city_name):
        json = requests.get('https://nominatim.openstreetmap.org/search?q=%s&format=json&polygon=1&addressdetails=1'%(city_name)).json()
        return json[0]['lat'], json[0]['lon']
