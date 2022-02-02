import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv('.env')
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
nutritionix_endpoint = os.environ.get("nutritionix_endpoint")
sheety_endpoint = os.environ.get("sheety_endpoint")


query_text = input("What kind of exercise have you done?: ")


# request header: contains authentication data
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}

# request body:
user_params = {
    "query": query_text,
    "gender": "female",
    "weight_kg": 47,
    "height_cm": 165,
    "age": 22
}

response = requests.post(url=nutritionix_endpoint, headers=headers, json=user_params)
data = response.json()
print(data['exercises'][0]["name"])

today_date = datetime.date(datetime.now()).strftime("%d/%m/%Y")
today_time = datetime.time(datetime.now()).strftime("%X")

sheet_header = {
    'Content-Type': 'application/json'
}

sheet_data = {
    "workout": {
        "date": today_date,
        "time": today_time,
        "exercise": data['exercises'][0]['name'],
        "duration": data['exercises'][0]['duration_min'],
        "calories": data['exercises'][0]['nf_calories']
    }
}

def add_new_data():
    sheety_response = requests.post(url=sheety_endpoint, headers=sheet_header, json=sheet_data)
    print(sheety_response.text)

add_new_data()