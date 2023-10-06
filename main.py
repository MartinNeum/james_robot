import logging, asyncio, threading, time, json, functools
from services import reminder_service, weather_service, setting_service, news_service
from handler import reminder_handler, setting_handler, weather_handler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, Updater, CommandHandler, CallbackQueryHandler
from decouple import config
from datetime import datetime, timedelta

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
DAILY_GREETING_HOUR = 5
DAILY_GREETING_MINUTE = 30

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s : %(message)s',
    level=logging.INFO,
    datefmt='%d.%m.%y um %H:%M:%S Uhr'
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f'Hi there, I am James! 👋 Please select a language:\n'

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="en"),
            InlineKeyboardButton("🇩🇪 Deutsch", callback_data="de"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup, parse_mode='Markdown')

async def set_user_chat_language(update: Update, context):
    query = update.callback_query
    await query.answer()

    try:
        user_setting = await setting_service.get_setting_by_chat_id(update.effective_chat.id)
        if user_setting is None:
            await setting_service._create_new_setting(update.effective_chat.id, update.effective_user.first_name, query.data, None, None, False)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Language setting already exists.", parse_mode='Markdown')

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.", parse_mode='Markdown')

    if query.data == "de":
        await query.edit_message_text(text=f"Willkommen, {update.effective_user.first_name}! 🤗")
    elif query.data == "en":
        await query.edit_message_text(text=f"Welcome, {update.effective_user.first_name}! 🤗")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "🤝 *Help*\n\nYou can use these commands to interact with me:"
    commands_text = "/help - Show avaliable commands\n /weather - Get the weather of a specified city\n /list - Show current reminders\n /remind - Create reminder\n /cancel - Cancel an existing reminder"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{header_text} \n\n {commands_text}",
        parse_mode='Markdown'
    )

async def good_morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        goodmorning = await get_goodmorning_string(update.effective_chat.id, update.effective_user.first_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=goodmorning, parse_mode='Markdown', disable_web_page_preview=True)

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.", parse_mode='Markdown')

async def get_goodmorning_string(chat_id, username):
    try:
        # Weather
        city = None
        with open(setting_service.SETTINGS_LIST, 'r') as file:
            settings = json.load(file)

        setting_exists = False
        for setting in settings:
            if setting['chat_id'] == chat_id:
                setting_exists = True
                city = setting['city']
                lang = setting['language']
                weather_info = await weather_service.get_weather_from_api(city, lang)

        if not setting_exists:
            weather_info = "_Weather: No city set. Use /setcity to get the weather._\n\n"

        # News
        news_info = await news_service.get_news_from_api()

        # Morning Text
        today = datetime.now()
        weekday = today.strftime("%A")
        day = today.strftime("%d")
        month = today.strftime("%B")
        year = today.strftime("%Y")

        goodmorning_message = f"🌅 *Good Morning, {username}!*\n\n"
        # goodmorning_message += f"Today is {weekday}, {month} {day}.\n\n"
        goodmorning_message += f"Today is {weekday}, {day} {month} {year}.\n\n"
        goodmorning_message += f"---\n"
        goodmorning_message += f"{weather_info}\n"
        goodmorning_message += f"---\n"
        goodmorning_message += f"{news_info}"
        goodmorning_message += f"Have a great start into the day! 😊\n_James_"

    except Exception as e:
        logging.error(str(e))
        await bot.send_message(chat_id=chat_id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.", parse_mode='Markdown')

    return goodmorning_message

async def check_reminders_job():
    while True:
        try:
            with open(reminder_service.REMINDERS_LIST, 'r') as file:
                reminders = json.load(file)

            current_time = int(time.time())

            for reminder in reminders:
                if reminder["reminder_time"] <= current_time:
                    await bot.send_message(chat_id=reminder["chat_id"], text=f"🔔 *Reminder:* {reminder['reminder_text']}", parse_mode='Markdown')
                    reminders.remove(reminder)

            with open(reminder_service.REMINDERS_LIST, 'w') as file:
                json.dump(reminders, file, indent=2)

        except Exception as e:
            logging.error(f"Error @ check_reminders_job: {str(e)}")

        await asyncio.sleep(30)

async def make_morning_greeting_job():
    while True:
        try:
            now = datetime.now()
            daily_message_time = datetime(now.year, now.month, now.day, DAILY_GREETING_HOUR, DAILY_GREETING_MINUTE, 0)

            if now >= daily_message_time:
                daily_message_time += timedelta(days=1)

            wait = daily_message_time - now
            await asyncio.sleep(wait.total_seconds())

            # Make Greeting
            with open(setting_service.SETTINGS_LIST, "r") as file:
                settings = json.load(file)

            for setting in settings:
                if setting['get_daily_greeting']:
                    morning_text = await get_goodmorning_string(setting['chat_id'], setting['username'])
                    await bot.send_message(chat_id=setting['chat_id'], text=morning_text, parse_mode='Markdown', disable_web_page_preview=True)

        except Exception as e:
            logging.error(str(e))
            await bot.send_message(chat_id=setting["chat_id"], text=f"😬 Sorry! Something went wrong with the daily update. Please tell the admin - thanks!", parse_mode='Markdown')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot = application.bot

    # GENERAL
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    goodmorning_handler = CommandHandler('goodmorning', good_morning)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(goodmorning_handler)
    application.add_handler(CallbackQueryHandler(set_user_chat_language))

    setting_command_handler = CommandHandler(['settings', 'set'], setting_handler.handle_request)
    reminder_command_handler = CommandHandler(['reminder'], reminder_handler.handle_request)
    weather_command_handler = CommandHandler(['weather'], weather_handler.handle_request)
    
    application.add_handlers([
        reminder_command_handler, 
        setting_command_handler,
        weather_command_handler
    ])

    # NEWS
    news_handler = CommandHandler('news', functools.partial(news_service.get_news))
    application.add_handler(news_handler)

    # Thread zur Überprüfung der Erinnerungen
    threading.Thread(target=lambda: asyncio.run(check_reminders_job()), daemon=True).start()
    threading.Thread(target=lambda: asyncio.run(make_morning_greeting_job()), daemon=True).start()

    application.run_polling()
