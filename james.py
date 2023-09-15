import logging
import asyncio
import threading
import time, json
import weather
import functools
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from decouple import config
from datetime import datetime

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
REMINDERS_LIST = 'reminders.json'

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s : %(message)s',
    level=logging.INFO,
    datefmt='%d.%m.%y um %H:%M:%S Uhr'
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there, I am James! 👋 How can I help you? \n_Use /help to see all avaliable commands_", parse_mode='Markdown')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="🤝 *Help* \n\nYou can use these commands to interact with me: \n\n /help - Show avaliable commands\n /list - Show current reminders\n /remind - Create reminder\n /cancel - Cancel an existing reminder",
        parse_mode='Markdown'
    )

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /remind*"
    syntax_text = "Please use this format: /remind `time` `text`"
    format_text = "• For `time` use m (minutes), h (hours), d (days) or w (weeks) \n • For `text` type any text you want James to tell you"
    example_text = "`/remind 2h Buy some Bananas 🍌` \n\nIn this example, James will send you a message in 2 hours with the text _'Buy some Bananas 🍌'._ "
    
    try:
        args = context.args
        if len(args) < 2:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return

        time_str = args[0]
        text = " ".join(args[1:])

        # Mapping der Zeiteinheiten
        time_units = {"m": 60, "h": 3600, "d": 86400, "w": 604800}  # Monate ungefähr, für Einfachheit

        unit = time_str[-1]
        if unit not in time_units:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="💬 Invalid time unit. Please use m, h, d, or w.")
            return

        try:
            duration = int(time_str[:-1]) * time_units[unit]
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="💬 Invalid time value. Please try again.")
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

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Success! ✅ Reminder set with ID:")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{reminder_id}")

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /cancel*"
    syntax_text = "Please use this format: /cancel `reminder_id`"
    format_text = "• For `reminder_id` paste the ID of the reminder you want to delete \n • _Hint: The ID was provided when you created the reminder_"
    example_text = "`/cancel 123` \n\nIn this example, James will remove the reminder with the ID '123'."
    
    try:
        args = context.args
        if len(args) != 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return

        chat_id_to_remove = int(args[0])

        # Durchsuchen der geplanten Erinnerungen und Entfernen derjenigen mit der angegebenen chat_id und reminder_id
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
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")


        if removed:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Success! ✅ Reminder removed.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Uuups! 🤔 No reminders found for the specified ID.")
    except Exception as e:
        logging.error(str(e))

async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reminders_text = "📃 *List of current Reminders*\n\n"
    hint_text = "\n_Timezone is UTC_ "
    
    try:
        with open(REMINDERS_LIST, 'r') as file:
            reminders = json.load(file)

        reminder_found = False
        
        for reminder in reminders:
            if reminder["chat_id"] == update.effective_chat.id:
                # Wandele den Timestamp in ein datetime-Objekt um und formatiere
                dt_object = datetime.fromtimestamp(reminder['reminder_time'])
                formatted_date_time = dt_object.strftime("%d.%m.%y at %H:%M")
                reminders_text += f"📌 '{reminder['text']}' ({formatted_date_time})\n"
                reminder_found = True

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")


    if reminder_found:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reminders_text + hint_text, parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="👏 It seems you're done for now. Enjoy your free time!")


async def check_reminders():
    while True:
        try:
            with open(REMINDERS_LIST, 'r') as file:
                reminders = json.load(file)
            
            current_time = int(time.time())
            
            for reminder in reminders:
                if reminder["reminder_time"] <= current_time:
                    # Sende die Erinnerungsnachricht hier
                    await bot.send_message(chat_id=reminder["chat_id"], text=f"🔔 *Reminder:* {reminder['text']}", parse_mode='Markdown')
                    # Entferne die Erinnerung aus der JSON-Datei
                    reminders.remove(reminder)
            
            with open(REMINDERS_LIST, 'w') as file:
                json.dump(reminders, file, indent=2)
        
        except Exception as e:
            logging.error(str(e))

        await asyncio.sleep(30)
  
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot = application.bot
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    reminder_handler = CommandHandler('remind', remind)
    cancel_handler = CommandHandler('cancel', cancel)
    list_handler = CommandHandler('list', list_reminders)
    weather_handler = CommandHandler('weather', functools.partial(weather.get_weather, bot=bot))

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(reminder_handler)
    application.add_handler(cancel_handler)
    application.add_handler(list_handler)
    application.add_handler(weather_handler)
    
    # Starten Sie den Thread zur Überprüfung der Erinnerungen
    threading.Thread(target=lambda: asyncio.run(check_reminders()), daemon=True).start()
    
    application.run_polling()
