import logging, json
from telegram import Update
from telegram.ext import ContextTypes

SETTINGS_LIST = 'settings.json'

async def set_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /setusername*"
    syntax_text = "Please use this format: /setusername `your_username`"
    format_text = "• For `your_username` paste your Username"
    example_text = "`/setusername Jürgen` \n\nIn this example, James will now call you _'Jürgen'_."

    try:
        args = context.args

        if len(args) != 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return

        username = args[0]
        setting_exists = False

        # Settings auslesen
        try:
            with open(SETTINGS_LIST, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = []

        try:
            # Finde Setting des Chats
            for setting in settings:
                if setting["chat_id"] == update.effective_chat.id:
                    setting_exists = True
                    setting["username"] = username

                with open(SETTINGS_LIST, 'w') as file:
                    json.dump(settings, file, indent=2)

            # Wenn kein Setting vorhanden, ein neues erstellen
            if not setting_exists:
                new_setting = {
                    "chat_id": update.effective_chat.id,
                    "username": username,
                    "location": None,
                    "get_daily_greeting": False
                }

                settings.append(new_setting)

                with open(SETTINGS_LIST, 'w') as file:
                    json.dump(settings, file, indent=2)

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ Hi there, {username}! 😊👋", parse_mode='Markdown')
        
    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")


async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /setlocation*"
    syntax_text = "Please use this format: /setusername `your_location`"
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

            # Wenn Setting nicht vorhanden, neu erstellen
            if not setting_exists:
                new_setting = {
                    "chat_id": update.effective_chat.id,
                    "username": None,
                    "location": location,
                    "get_daily_greeting": False
                }

                settings.append(new_setting)

                with open(SETTINGS_LIST, 'w') as file:
                    json.dump(settings, file, indent=2)

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

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

            # Wenn Setting nicht vorhanden, neu erstellen
            if not setting_exists:
                new_setting = {
                    "chat_id": update.effective_chat.id,
                    "username": None,
                    "location": None,
                    "get_daily_greeting": want_greeting
                }

                settings.append(new_setting)

                with open(SETTINGS_LIST, 'w') as file:
                    json.dump(settings, file, indent=2)

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

        if want_greeting:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ You will now get a daily update form me 🗞", parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ You won't get any more daily updates.", parse_mode='Markdown')
        
    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")


async def get_settings(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    header_text = "⚙️ *Settings*"
    settings_text = ""

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
                    get_greeting = "Yes" if setting['get_daily_greeting'] else "No"
                    settings_text += f"🙍‍♂️ Username: _{setting['username']}_\n 📍 Location: _{setting['location']}_\n 📰 Daily Update: _{get_greeting}_"

                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {settings_text}", parse_mode='Markdown')
                return
            
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🤷‍♂️ I could not find any settings yet. Help me to get to know you better: \n\n • /setusername\n • /setlocation\n • /setdailygreeting", parse_mode='Markdown')

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")