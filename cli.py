import requests
import argparse
import sys

api_Key = '354ecbe28e3ed8ec12bd0c76e87369f8'
api_Url = 'https://api.openweathermap.org/data/2.5/weather'
units = 'metric'

parser = argparse.ArgumentParser()
parser.add_argument("--city", default="Minsk")
parser.add_argument("--lat", type=int, default=1)
parser.add_argument("--lon", type=int, default=1)
parser.add_argument("--units", type=str, default='metric')
namespace = parser.parse_args()

print(namespace)


def current_weather(location, units, api_key=api_Key):
    params = {'q': location, 'appid': api_key, 'units': units}
    response = requests.get(api_Url, params=params)
    response = response.json()
    print(response)
    return response

response = current_weather(location=namespace.city, units=namespace.units)
print(f'\nCity = {response["name"]}\ncountry = {response["sys"]["country"]}\ntemp = {response["main"]["temp"]}')
