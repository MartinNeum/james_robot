import logging, asyncio
from services import messagetext_service, setting_service, weather_service, news_service
from handler import weather_handler, general_handler
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

DAILY_GREETING_HOUR = 21
DAILY_GREETING_MINUTE = 31

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    incomming_endpoint = update.message.text.split()[0]

    if incomming_endpoint == '/start':
        req_response = f"Hi {update.effective_user.first_name}, I am James! 👋 How can I help you? \n_Hint: Use /help to see all avaliable commands_"

    elif incomming_endpoint == '/help':
        req_response = messagetext_service.GENERAL['help']

    elif incomming_endpoint == '/goodmorning':
        req_response = await _prepare_goodmorning_text(update.effective_chat.id, update.effective_user.first_name)

    else:
        req_response = "Please insert a valid endpoint."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=req_response, parse_mode='Markdown', disable_web_page_preview=True)

async def _prepare_goodmorning_text(chat_id, username):
    try:
        setting = await setting_service._get_setting_by_chat_id(chat_id)
        if setting is None: setting = await setting_service.initialize_user_setting(chat_id, username)
        
        # Get day
        today = datetime.now()
        weekday = today.strftime("%A")
        day = today.strftime("%d")
        month = today.strftime("%B")
        year = today.strftime("%Y")

        text = f"👋 *Good Morning, {username}!* \nToday is {weekday}, {day} {month} {year}.\n\n\n"

        # Get weather
        if setting['city'] is not None:
            weather_data = await weather_service.get_weather(setting['city'])
            text += await weather_handler._prepare_response_text(weather_data) + "\n\n"
        else:
            text += "_Weather: No city set. Use `/set city your-city` to get the weather._\n\n\n"

        # Get news
        text += await news_service.get_news()

        text += "Have a great day! 🤗"

        return text

    except Exception as e:
        logging.error(str(e))
        return messagetext_service.GENERAL['error']
    
async def _do_daily_update_job(bot):
    while True:
        try:
            now = datetime.now()
            daily_message_time = datetime(now.year, now.month, now.day, DAILY_GREETING_HOUR, DAILY_GREETING_MINUTE, 0)

            if now >= daily_message_time:
                daily_message_time += timedelta(days=1)

            wait = daily_message_time - now
            await asyncio.sleep(wait.total_seconds())

            settings = await setting_service._get_all_settings()
            for setting in settings:
                if setting['get_daily']:
                    chat_id = setting['chat_id']
                    username = setting['username']
                    text = await general_handler._prepare_goodmorning_text(chat_id, username)
                    await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown', disable_web_page_preview=True)

        except Exception as e:
            logging.error(str(e))
            await bot.send_message(chat_id=chat_id, text=f"😬 Sorry! Something went wrong with the daily update. Please tell the admin - thanks!", parse_mode='Markdown')
