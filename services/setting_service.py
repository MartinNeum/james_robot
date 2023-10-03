import logging, json
from telegram import Update
from telegram.ext import ContextTypes

SETTINGS_LIST = 'settings.json'
DEFAULT_LANGUAGE = 'en'
DEFAULT_COUNTRY = 'us'
POSSIBLE_COUNTRIES = ['ger', 'us']

async def set_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /setcity*"
    syntax_text = "Please use this format: /setcity `your_city`"
    format_text = "• For `your_city` paste your city"
    example_text = "`/setcity Berlin` \n\nIn this example, James will now use your loaction _'Berlin'_."

    try:
        args = context.args

        if len(args) != 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return

        city = args[0]
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
                    setting["city"] = city

                    with open(SETTINGS_LIST, 'w') as file:
                        json.dump(settings, file, indent=2)

            if not setting_exists: await create_new_setting(update.effective_chat.id, update.effective_user.first_name, DEFAULT_LANGUAGE, city, None, False)

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

        # Response senden
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ Looks very nice here, in {city}! 🗺", parse_mode='Markdown')
        
    except Exception as e:
        logging.error(str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

async def set_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header_text = "⚙️ *How to: /setcountry*"
    syntax_text = "Please use this format: /setcountry `your_country`"
    format_text = "• For `your_country` paste your country"
    example_text = "`/setcountry ger` \n\nIn this example, James will now use your country _'Germany'_."

    try:
        args = context.args

        if len(args) != 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{header_text}\n\n {syntax_text}\n\n *Parameters*\n {format_text}\n\n *Example*\n {example_text}", parse_mode='Markdown')
            return

        country = args[0]
        if country not in POSSIBLE_COUNTRIES:
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
                    setting["country"] = country

                    with open(SETTINGS_LIST, 'w') as file:
                        json.dump(settings, file, indent=2)

            if not setting_exists: await create_new_setting(update.effective_chat.id, update.effective_user.first_name, DEFAULT_LANGUAGE, None, country, False)

        except Exception as e:
            logging.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😬 Sorry! There is an internal error. Please try again or contact the admin.")

        # Response senden
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Success! ✅ {country} looks like a very beautiful place! 🗺", parse_mode='Markdown')
        
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

            if not setting_exists: await create_new_setting(update.effective_chat.id, update._effective_user.first_name, DEFAULT_LANGUAGE, None, None, want_greeting)

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
                    settings_text += f"💬 Language: _{setting['language']}_\n 📍 City: _{setting['city']}_\n 🌍 Country: {setting['country']}\n 📰 Daily Update: _{get_greeting}_"

            if not setting_exists: 
                new = await create_new_setting(update.effective_chat.id, update.effective_user.first_name, DEFAULT_LANGUAGE, None, None, False)
                settings_text += f"💬 Language: _{DEFAULT_LANGUAGE}_\n 📍 City: _{new['city']}_\n 🌍 Country: _None_\n 📰 Daily Update: _No_"
            
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
async def create_new_setting(chat_id, username, language, city, country, get_daily_greeting):
    try:
        with open(SETTINGS_LIST, 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = []
    
    new_setting = {
        "chat_id": chat_id,
        "username": username,
        "language": language,
        "city": city,
        "country": country,
        "get_daily_greeting": get_daily_greeting
    }

    settings.append(new_setting)

    with open(SETTINGS_LIST, 'w') as file:
        json.dump(settings, file, indent=2)

    return new_setting

async def get_setting_by_chat_id(chat_id):
    try:
        with open(SETTINGS_LIST, 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = []

    for setting in settings:
        if setting['chat_id'] == chat_id:
            return setting
        
    return None