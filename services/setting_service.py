import logging, json
from telegram import Update
from telegram.ext import ContextTypes

SETTINGS_LIST = 'settings.json'
DEFAULT_LANGUAGE = 'en'

async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /setlocation*"
    syntax_text = "Please use this format: /setlocation `your_location`"
    format_text = "• For `your_location` paste your location"
    example_text = "`/setlocation Berlin` \n\nIn this example, James will now use your loaction _'Berlin'_."

    try:
        args = context.args

        if len(args) != 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return

        location = args[0]
        setting_exists = False

        # Settings auslesen
        try:
            with open(SETTINGS_LIST, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = []

        try:
            # Suche Setting und ändere Daten
            for setting in settings:
                if setting["chat_id"] == update.effective_chat.id:
                    setting_exists = True
                    setting["location"] = location

                    with open(SETTINGS_LIST, 'w') as file:
                        json.dump(settings, file, indent=2)

            if not setting_exists: await create_new_setting(update.effective_chat.id, update.effective_user.first_name, DEFAULT_LANGUAGE, location, False)

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

        # Response senden
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ Looks very nice here, in {location}! 🗺", parse_mode='Markdown')
        
    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")


async def set_daily_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    header_text = "⚙️ *How to: /setdailygreeting*"
    syntax_text = "Please use this format: /setdailygreeting `yes/no`"
    format_text = "• For `yes/no` paste 'yes' or 'no'"
    example_text = "`/setdailygreeting yes` \n\nIn this example, James will now greet you every morning with some useful information about the day."

    try:
        args = context.args

        if len(args) != 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return

        want_greeting = args[0]
        if want_greeting == "yes":
            want_greeting = True
        elif want_greeting == "no":
            want_greeting = False
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return

        setting_exists = False

        # Settings auslesen
        try:
            with open(SETTINGS_LIST, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = []

        try:
            # Suche Setting und ändere Daten
            for setting in settings:
                if setting["chat_id"] == update.effective_chat.id:
                    setting_exists = True
                    setting["get_daily_greeting"] = want_greeting

                    with open(SETTINGS_LIST, 'w') as file:
                        json.dump(settings, file, indent=2)

            if not setting_exists: await create_new_setting(update.effective_chat.id, update._effective_user.first_name, DEFAULT_LANGUAGE, None, want_greeting)

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

        # Response senden
        if want_greeting:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ You will now get a daily update from me 🗞", parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ You won't get any more daily updates.", parse_mode='Markdown')
        
    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")


async def get_settings(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    header_text = f"⚙️ *{update.effective_user.first_name}'s Settings*"
    settings_text = ""
    setting_exists = False

    try:
        # Settings auslesen
        try:
            with open(SETTINGS_LIST, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = []

        try:
            for setting in settings:
                if setting["chat_id"] == update.effective_chat.id:
                    setting_exists = True
                    get_greeting = "Yes" if setting['get_daily_greeting'] else "No"
                    settings_text += f"💬 Language: _{setting['language']}_\n 📍 Location: _{setting['location']}_\n 📰 Daily Update: _{get_greeting}_"

            if not setting_exists: 
                new = await create_new_setting(update.effective_chat.id, update.effective_user.first_name, DEFAULT_LANGUAGE, None, False)
                settings_text += f"📍 Location: _{new['location']}_\n 📰 Daily Update: _No_"
            
        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

        # Response senden
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {settings_text}", parse_mode='Markdown')

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

# 
# Helper functions
# 
async def create_new_setting(chat_id, username, language, location, get_daily_greeting):
    try:
        with open(SETTINGS_LIST, 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = []
    
    new_setting = {
        "chat_id": chat_id,
        "username": username,
        "language": language,
        "location": location,
        "get_daily_greeting": get_daily_greeting
    }

    settings.append(new_setting)

    with open(SETTINGS_LIST, 'w') as file:
        json.dump(settings, file, indent=2)

    return new_setting