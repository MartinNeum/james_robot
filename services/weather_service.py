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

# async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     header_text = "⚙️ *How to: /weather*"
#     syntax_text = "Please use this format: /weather `city`"
#     format_text = "• For `city` paste your current city"
#     example_text = "`/weather Berlin` \n\nIn this example, James will inform you about the current weather in Berlin."
#     hint_text = "_Hint: Use /city to let me know your city. You then dont need to specify your city in future anymore 😉_"

#     args = context.args

#     # Zu viele Argumente geliefert
#     if len(args) > 1:
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
#         return
    
#     # Setting auslesen
#     user_setting = await setting_service.get_setting_by_chat_id(update.effective_chat.id)
#     if user_setting is not None:
#         user_language = user_setting.get('language', setting_service.DEFAULT_LANGUAGE)
#     else:
#         user_language = setting_service.DEFAULT_LANGUAGE

#     # Stadt geliefert
#     if len(args) == 1:
#         request_city = args[0]

#         response_text = await get_weather_from_api(request_city, user_language)
        
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{response_text}\n\n{hint_text}", parse_mode='Markdown')
#         return
    
#     # Stadt nicht geliefert, Settings prüfen
#     else:
#         try:
#             user_city = None
#             with open(setting_service.SETTINGS_LIST, 'r') as file:
#                 settings = json.load(file)

#                 for setting in settings:
#                     if setting["chat_id"] == update.effective_chat.id:
#                         user_city = setting["city"]

#                 if not user_city == None:
#                     response_text = await get_weather_from_api(user_city, user_language)
#                 else:
#                     await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
#                     return

#             await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text, parse_mode='Markdown')
#             return

#         except Exception as e:
#             logging.error(str(e))
#             await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

# async def get_weather_from_api(city, language):
#     url = f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_TOKEN}&q={city}&days=3&aqi=no&alerts=yes&lang={language}'
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()

#         city_name = data['location']['name']
#         city_region = data['location']['region']
#         # Check Alerts
#         alert_text = ''
#         for alert in data['alerts']['alert']:
#             alert_text += f'\n⚠️ *Warning: {alert["headline"]}*\n'
#             alert_text += f'_Category: {alert["category"]}_\n'
#             alert_text += f'_Description: {alert["desc"]}_\n'
#         # Current Weather
#         current_weather_description = data['current']['condition']['text']
#         current_temperature = data['current']['temp_c']
#         current_wind = data['current']['wind_kph']
#         # Today Weather
#         today_weather_description = data['forecast']['forecastday'][0]['day']['condition']['text']
#         today_temperature = data['forecast']['forecastday'][0]['day']['maxtemp_c']
#         today_chanceof_rain = data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']

#         response_text = f"*Weather* • _{city_name}_\n"
#         response_text += f"{alert_text}\n"
#         response_text += f"*Today*\n"
#         response_text += f"☀️ {today_weather_description} • 🌡 {today_temperature}°C • ☔️ {today_chanceof_rain}%\n\n"
#         response_text += f"📆 *Forecast*\n"

#         i = 0
#         for day in data['forecast']['forecastday']:
#             if i == 0: 
#                 i += 1
#                 continue
#             else:
#                 tmp_date = datetime.strptime(day['date'], '%Y-%m-%d')
#                 forecast_date = tmp_date.strftime('%d.%m')
                
#                 response_text += f"_{forecast_date}_: "

#                 forecast_weather_description = data['forecast']['forecastday'][i]['day']['condition']['text']
#                 forecast_temperature = data['forecast']['forecastday'][i]['day']['maxtemp_c']
#                 forecast_chanceof_rain = data['forecast']['forecastday'][i]['day']['daily_chance_of_rain']

#                 response_text += f"{forecast_weather_description} • {forecast_temperature}°C • {forecast_chanceof_rain}%\n"
#                 i += 1

#     else:
#         response_text = "😬 Sorry! There is an internal error. Please try again or contact the admin."
    
#     return response_text
