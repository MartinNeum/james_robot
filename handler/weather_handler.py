from datetime import datetime
from services import messagetext_service, weather_service, setting_service
from telegram import Update
from telegram.ext import ContextTypes

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    provided_city = context.args[0] if context.args else None
    chat_id = update.effective_chat.id

    # Check Setting
    setting = await setting_service.get_user_setting(chat_id)
    if setting is None:
        setting = await setting_service.initialize_user_setting(chat_id, update.effective_user.first_name)

    if provided_city:
        data = await weather_service.get_weather(provided_city)
        req_response = await _prepare_response_text(data)
        req_response += messagetext_service.WEATHER['hint']
    elif setting['city']:
        data = await weather_service.get_weather(setting['city'])
        req_response = await _prepare_response_text(data)
    else:
        req_response = messagetext_service.WEATHER['how_to']

    await context.bot.send_message(chat_id=chat_id, text=req_response, parse_mode='Markdown')

async def _prepare_response_text(data):
    text = f"🌤 *Weather* • _{data['city_name']}_\n\n"

    for alert in data['alerts']:
        text += f"⚠️ *Warning: {alert['headline']}*\n"
        alert_desc = alert['desc'].replace('\n', " ")
        text += f"Category: {alert['category']}  •  Description: {alert_desc}\n\n"

    i=0
    for day in data['data']:
        desc = day['day']['condition']['text']
        temp = day['day']['maxtemp_c']
        chance_rain = day['day']['daily_chance_of_rain']
        if i == 0: text += f"Today \n"
        elif i == 1: text += f"Forecast \n"
        if i > 0:
            tmp_date = datetime.strptime(day['date'], '%Y-%m-%d')
            forecast_date = tmp_date.strftime('%d.%m')
            text += f"{forecast_date}: "
        
        text += f"{desc} • 🌡 {temp} °C • ☔️ {chance_rain} %\n"
        if i == 0: text += f"\n"

        i += 1

    return text
