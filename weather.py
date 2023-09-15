import requests
from telegram import Update
from telegram.ext import ContextTypes
from decouple import config

WEATHER_API_TOKEN = config('WEATHER_API_TOKEN')

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE, bot):
    # Die Nachricht des Benutzers in der Form "/weather Stadt" aufteilen
    message_text = update.message.text
    parts = message_text.split(' ')

    header_text = "⚙️ *How to: /weather*"
    syntax_text = "Please use this format: /weather `city`"
    format_text = "• For `city` paste your current city location"
    example_text = "`/weather Berlin` \n\nIn this example, James will inform you about the current weather in Berlin."

    if len(parts) != 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
        return

    request_city = parts[1]
    api_key = WEATHER_API_TOKEN

    # Die API-Anfrage an weatherapi.com senden
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={request_city}&aqi=no'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        location_name = data['location']['name']
        location_region = data['location']['region']
        weather_description = data['current']['condition']['text']
        temperature_celsius = data['current']['temp_c']
        feelslike_celsius = data['current']['feelslike_c']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']

        response_text = f"*Weather (Current)*\n"
        response_text += f"_{location_name}, {location_region}_\n\n"
        response_text += f"{weather_description}\n\n"
        response_text += f"🌡 {temperature_celsius} °C\n"
        response_text += f"💆‍♂️ feels like {feelslike_celsius} °C\n"
        response_text += f"💧 {humidity} %\n"
        response_text += f"💨 {wind_kph} km/h"

    else:
        response_text = "😬 Sorry! There is an internal error. Please try again or contact the admin."

    await bot.send_message(chat_id=update.effective_chat.id, text=response_text, parse_mode='Markdown')