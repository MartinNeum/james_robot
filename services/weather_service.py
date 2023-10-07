import requests, json, logging
from services import setting_service
from telegram import Update
from telegram.ext import ContextTypes
from decouple import config
from datetime import datetime

WEATHER_API_TOKEN = config('WEATHER_API_TOKEN')

async def get_weather(city):
    url = f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_TOKEN}&q={city}&days=3&aqi=no&alerts=yes&'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            return {
                "city_name": data['location']['name'],
                "alerts": data['alerts']['alert'],
                "data": data['forecast']['forecastday']
            }
        except Exception as e:
            logging.error(str(e))
            return None

    else:
        return None
