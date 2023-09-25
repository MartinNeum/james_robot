import logging, asyncio, threading, time, json, functools
from services import reminder_service, weather_service
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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there, I am James! 👋 How can I help you? \n_Use /help to see all avaliable commands_", parse_mode='Markdown')

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
                    await bot.send_message(chat_id=reminder["chat_id"], text=f"🔔 *Reminder:* {reminder['text']}", parse_mode='Markdown')
                    reminders.remove(reminder)
            
            with open(reminder_service.REMINDERS_LIST, 'w') as file:
                json.dump(reminders, file, indent=2)
        
        except Exception as e:
            logging.error(str(e))

        await asyncio.sleep(30)
  
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot = application.bot
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    reminder_handler = CommandHandler('remind', reminder_service.remind)
    cancel_handler = CommandHandler('cancel', reminder_service.cancel)
    list_handler = CommandHandler('list', reminder_service.list_reminders)
    weather_handler = CommandHandler('weather', functools.partial(weather_service.get_weather, bot=bot))

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(reminder_handler)
    application.add_handler(cancel_handler)
    application.add_handler(list_handler)
    application.add_handler(weather_handler)
    
    # Thread zur Überprüfung der Erinnerungen
    threading.Thread(target=lambda: asyncio.run(check_reminders()), daemon=True).start()
    
    application.run_polling()
