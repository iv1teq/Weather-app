import requests

from config import API_KEY
import json 
from modules import Search


def api_request(city_name: str):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={API_KEY}")
    data_dict = response.json()
    with open(f"static/json/{city_name}.json", mode ="w")as file:
        json.dump(obj = data_dict, fp = file, indent = 4, ensure_ascii = False)





    
    return data_dict
