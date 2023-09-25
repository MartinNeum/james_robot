import requests, json, logging
from services import setting_service
from telegram import Update
from telegram.ext import ContextTypes
from decouple import config
from datetime import datetime

WEATHER_API_TOKEN = config('WEATHER_API_TOKEN')

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /weather*"
    syntax_text = "Please use this format: /weather `city`"
    format_text = "• For `city` paste your current city location"
    example_text = "`/weather Berlin` \n\nIn this example, James will inform you about the current weather in Berlin."
    hint_text = "_Hint: Use /setlocation to let me know your location. You then dont need to specify your location in future anymore 😉_"

    args = context.args

    # Zu viele Argumente geliefert
    if len(args) > 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
        return
    
    # Stadt geliefert
    if len(args) == 1:
        request_city = args[0]

        response_text = await get_weather_from_api(request_city)
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{response_text}\n\n{hint_text}", parse_mode='Markdown')
        return
    
    # Stadt nicht geliefert, Settings prüfen
    else:
        try:
            user_location = None
            with open(setting_service.SETTINGS_LIST, 'r') as file:
                settings = json.load(file)

                for setting in settings:
                    if setting["chat_id"] == update.effective_chat.id:
                        user_location = setting["location"]

                if not user_location == None:
                    response_text = await get_weather_from_api(user_location)
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
                    return

            await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text, parse_mode='Markdown')
            return

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

async def get_weather_from_api(city):
    url = f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_TOKEN}&q={city}&days=4&aqi=no&alerts=no'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        location_name = data['location']['name']
        location_region = data['location']['region']
        # Current Weather
        current_weather_description = data['current']['condition']['text']
        current_temperature = data['current']['temp_c']
        current_wind = data['current']['wind_kph']
        # Today Weather
        today_weather_description = data['forecast']['forecastday'][0]['day']['condition']['text']
        today_temperature = data['forecast']['forecastday'][0]['day']['avgtemp_c']
        today_chanceof_rain = data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
        today_wind = data['forecast']['forecastday'][0]['day']['maxwind_kph']

        response_text = f"*Weather*\n"
        response_text += f"_{location_name}, {location_region}_\n\n"
        response_text += f"*Today*\n"
        response_text += f"☀️ {today_weather_description} • 🌡 {today_temperature}°C • ☔️ {today_chanceof_rain}% • 💨 {today_wind} km/h\n\n"
        # response_text += f"☀️ {today_weather_description}\n 🌡 {today_temperature}°C\n ☔️ {today_chanceof_rain}%\n 💨 {today_wind} km/h\n\n"
        response_text += f"📆 *Forecast*\n"

        i = 0
        for day in data['forecast']['forecastday']:
            if i == 0: 
                i += 1
                continue
            else:
                tmp_date = datetime.strptime(day['date'], '%Y-%m-%d')
                forecast_date = tmp_date.strftime('%d.%m')
                
                response_text += f"_{forecast_date}_: "

                forecast_weather_description = data['forecast']['forecastday'][i]['day']['condition']['text']
                forecast_temperature = data['forecast']['forecastday'][i]['day']['avgtemp_c']
                forecast_chanceof_rain = data['forecast']['forecastday'][i]['day']['daily_chance_of_rain']
                forecast_wind = data['forecast']['forecastday'][i]['day']['maxwind_kph']

                response_text += f"{forecast_weather_description} • {forecast_temperature}°C • {forecast_chanceof_rain}% • {forecast_wind} km/h\n"
                # response_text += f"☀️ {forecast_weather_description}\n 🌡 {forecast_temperature}°C\n ☔️ {forecast_chanceof_rain}%\n 💨 {forecast_wind} km/h\n\n"
                i += 1

    else:
        response_text = "😬 Sorry! There is an internal error. Please try again or contact the admin."
    
    return response_text
