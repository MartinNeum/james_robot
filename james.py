import logging
import asyncio
import threading
import time, json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from decouple import config
from datetime import datetime

TOKEN = config('TELEGRAM_TOKEN')
REMINDERS_LIST = 'reminders.json'

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s : %(message)s',
    level=logging.INFO,
    datefmt='%d.%m.%y um %H:%M:%S Uhr'
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there, I am James! 👋 How can I help you?", parse_mode='Markdown')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="ℹ️ *Help* \n\nYou can use these commands to interact with me: \n\n /help - Show avaliable commands",
        parse_mode='Markdown'
    )

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /remind <time> <text>")
            return

        time_str = args[0]
        text = " ".join(args[1:])

        # Mapping der Zeiteinheiten
        time_units = {"m": 60, "h": 3600, "d": 86400, "w": 604800}  # Monate ungefähr, für Einfachheit

        unit = time_str[-1]
        if unit not in time_units:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid time unit. Use m, h, d, or w.")
            return

        try:
            duration = int(time_str[:-1]) * time_units[unit]
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid time value.")
            return
        
        # Reminder erstellen und speichern
        reminder_id = int(time.time())
        new_reminder = {
            "id": reminder_id,
            "chat_id": update.effective_chat.id,
            "reminder_time": int(time.time()) + duration,
            "text": text
        }
    
        # Lade vorhandene Erinnerungen aus der JSON-Datei (falls vorhanden)
        try:
            with open('reminders.json', 'r') as file:
                reminders = json.load(file)
        except FileNotFoundError:
            reminders = []

        # Füge den neuen Reminder zur Liste hinzu
        reminders.append(new_reminder)

        # Speichere die aktualisierten Erinnerungen zurück in die JSON-Datei
        with open('reminders.json', 'w') as file:
            json.dump(reminders, file, indent=2)

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Success! Reminder set with ID:")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{reminder_id}")

    except Exception as e:
        logging.error(str(e))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /cancel <reminder_id>")
            return

        chat_id_to_remove = int(args[0])

        # Durchsuchen der geplanten Erinnerungen und Entfernen derjenigen mit der angegebenen chat_id
        removed = False
        try:
            with open(REMINDERS_LIST, 'r') as file:
                reminders = json.load(file)
            
            for reminder in reminders:
                if reminder["chat_id"] == update.effective_chat.id and chat_id_to_remove == reminder["id"]:
                    reminders.remove(reminder)
                    removed = True

            with open(REMINDERS_LIST, 'w') as file:
                json.dump(reminders, file, indent=2)
        
        except Exception as e:
            print(f"Fehler beim Überprüfen der Erinnerungen: {str(e)}")

        if removed:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Success! Reminder removed.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No reminders found for the specified chat_id.")
    except Exception as e:
        logging.error(str(e))

async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reminders_text = "Current reminders:\n\n"
    
    try:
        with open(REMINDERS_LIST, 'r') as file:
            reminders = json.load(file)

        reminder_found = False
        
        for reminder in reminders:
            if reminder["chat_id"] == update.effective_chat.id:
                # Wandele den Timestamp in ein datetime-Objekt um und formatiere
                dt_object = datetime.fromtimestamp(reminder['reminder_time'])
                formatted_date_time = dt_object.strftime("%d.%m.%y um %H:%M Uhr")
                reminders_text += f"'{reminder['text']}' , set for {formatted_date_time}\n"
                reminder_found = True

    except Exception as e:
        print(f"Fehler beim Überprüfen der Erinnerungen: {str(e)}")

    if reminder_found:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reminders_text)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Currently no reminders set.")


async def check_reminders():
    while True:
        try:
            with open(REMINDERS_LIST, 'r') as file:
                reminders = json.load(file)
            
            current_time = int(time.time())
            
            for reminder in reminders:
                if reminder["reminder_time"] <= current_time:
                    # Sende die Erinnerungsnachricht hier
                    await bot.send_message(chat_id=reminder["chat_id"], text=f"Reminder: {reminder['text']}")
                    # Entferne die Erinnerung aus der JSON-Datei
                    reminders.remove(reminder)
            
            with open(REMINDERS_LIST, 'w') as file:
                json.dump(reminders, file, indent=2)
        
        except Exception as e:
            print(f"Fehler beim Überprüfen der Erinnerungen: {str(e)}")

        await asyncio.sleep(30)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    bot = application.bot
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    reminder_handler = CommandHandler('remind', remind)
    cancel_handler = CommandHandler('cancel', cancel)
    list_handler = CommandHandler('list', list_reminders)
    
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(reminder_handler)
    application.add_handler(cancel_handler)
    application.add_handler(list_handler)
    
    # Starten Sie den Thread zur Überprüfung der Erinnerungen
    threading.Thread(target=lambda: asyncio.run(check_reminders()), daemon=True).start()
    
    application.run_polling()
