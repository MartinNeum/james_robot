import logging, asyncio, threading
from services import reminder_service
from handler import reminder_handler, setting_handler, weather_handler, news_handler, general_handler
from telegram.ext import ApplicationBuilder, CommandHandler
from decouple import config

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s : %(message)s',
    level=logging.INFO,
    datefmt='%d.%m.%y um %H:%M:%S Uhr'
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot = application.bot

    # Handlers
    general_command_handler = CommandHandler(['start', 'help', 'goodmorning'], general_handler.handle_request)
    setting_command_handler = CommandHandler(['settings', 'set'], setting_handler.handle_request)
    reminder_command_handler = CommandHandler(['reminder'], reminder_handler.handle_request)
    weather_command_handler = CommandHandler(['weather'], weather_handler.handle_request)
    news_command_handler = CommandHandler(['news'], news_handler.handle_request)
    
    application.add_handlers([
        reminder_command_handler, 
        setting_command_handler,
        weather_command_handler,
        news_command_handler,
        general_command_handler
    ])

    # Jobs
    threading.Thread(target=lambda: asyncio.run(reminder_service._do_reminders_job(bot)), daemon=True).start()
    threading.Thread(target=lambda: asyncio.run(general_handler._do_daily_update_job(bot)), daemon=True).start()

    application.run_polling()
