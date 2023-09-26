import logging, asyncio, threading, time, json, functools
from services import reminder_service, weather_service, setting_service, shopping_service
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from decouple import config

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s : %(message)s',
    level=logging.INFO,
    datefmt='%d.%m.%y um %H:%M:%S Uhr'
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {update.effective_user.first_name}, I am James! 👋 How can I help you? \n_Use /help to see all avaliable commands_", parse_mode='Markdown')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "🤝 *Help*\n\nYou can use these commands to interact with me:"
    commands_text = "/help - Show avaliable commands\n /weather - Get the weather of a specified city\n /list - Show current reminders\n /remind - Create reminder\n /cancel - Cancel an existing reminder"
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"{header_text} \n\n {commands_text}",
        parse_mode='Markdown'
    )

async def check_reminders():
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
            logging.error(str(e))

        await asyncio.sleep(30)
  
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot = application.bot
    
    # GENERAL
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    application.add_handler(start_handler)
    application.add_handler(help_handler)

    # SETTINGS
    set_location_handler = CommandHandler('setlocation', setting_service.set_location)
    set_daily_greeting_handler = CommandHandler('setdailygreeting', setting_service.set_daily_greeting)
    settings_handler = CommandHandler('settings', setting_service.get_settings)
    application.add_handler(set_location_handler)
    application.add_handler(set_daily_greeting_handler)
    application.add_handler(settings_handler)

    # REMINDER
    reminder_handler = CommandHandler('remind', reminder_service.remind)
    cancel_handler = CommandHandler('cancel', reminder_service.cancel)
    list_handler = CommandHandler('list', reminder_service.list_reminders)
    application.add_handler(reminder_handler)
    application.add_handler(cancel_handler)
    application.add_handler(list_handler)

    # SHOPPINGLIST
    add_items_handler = CommandHandler('add', shopping_service.add_items)
    remove_items_handler = CommandHandler('remove', shopping_service.remove_items)
    get_shoppinglist_handler = CommandHandler('shoppinglist', shopping_service.get_shoppinglist)
    clear_shoppinglist_handler = CommandHandler('clear', shopping_service.clear_shoppinglist)
    application.add_handler(add_items_handler)
    application.add_handler(remove_items_handler)
    application.add_handler(get_shoppinglist_handler)
    application.add_handler(clear_shoppinglist_handler)

    # WEATHER
    weather_handler = CommandHandler('weather', functools.partial(weather_service.get_weather))
    application.add_handler(weather_handler)
    
    # Thread zur Überprüfung der Erinnerungen
    threading.Thread(target=lambda: asyncio.run(check_reminders()), daemon=True).start()
    
    application.run_polling()
