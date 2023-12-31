GENERAL = {
    "error": "😬 Sorry! There is an internal error. Please try again or contact the admin.",
    "help": "🙋‍♂️ *Help*\n\nYou can use these commands to interact with me: \n\n*General* \n/help - Show avaliable commands \n/goodmorning - Get good-morning-message \n\n*Settings* \n/settings - Show your settings \n/set city your-city - Set your city \n/set dailyupdate yes/no - Let me know if you want a daily update \n\n*Reminder* \n/reminder set time text - Set a reminder \n/reminder cancel reminder-ID - Cancel a reminder \n/reminder list - Get a list of all reminders \n\n*Weather* \n/weather - If you have set your city, get the weather \n/weather city - Get the weather of a specified city \n\n*News* \n/news - Get some headlines"
}

REMINDER = {
    "how_to": "⚙️ *How To: /reminder* \n\nOptions\n • set: /reminder set time text\n • cancel: /reminder cancel reminder-ID\n • list: /reminder list",
    "how_to_set": "⚙️ *How To: /reminder set*\n\n Please use this format: /reminder set `time` `text`\n\n Parameters\n • For `time` use m (minutes), h (hours), d (days) or w (weeks) \n • For `text` type any text you want James to tell you \n\nExample\n /reminder set 2h Buy some Bananas 🍌 \n\nIn this example, James will send you a message in 2 hours with the text _'Buy some Bananas 🍌'._",
    "how_to_cancel": "⚙️ *How To: /reminder cancel* \n\nPlease use this format: /reminder cancel `reminder-ID` \n\nParameters\n • For `reminder-ID` paste the ID of the reminder \n\nExample\n /reminder cancel 123 \n\nIn this example, James will cancel the reminder with the ID 123.",
    "invalid_time_unit": "💬 Invalid time unit. Please use m, h, d, or w.",
    "invalid_time_value": "💬 Invalid time value. Please try again.",
    "reminder_not_found": "Uuups! 🤔 No reminders found for the specified ID.",
    "empty_reminder_list": "👏 It seems you're done for now. Enjoy your free time!",
    "success_new_reminder": "Success! ✅ Reminder set with ID:",
    "success_reminder_removed": "Success! ✅ Reminder removed."
}

SETTING = {
    "how_to": "⚙️ *How To: /set* \n\nOptions \n• city: /set city your-city \n• dailyupdate: /set dailyupdate yes/no",
    "how_to_city": "⚙️ *How To: /set city* \n\nPlease use this format: /set city `your_city` \n\nParameters \n• For `your_city` paste your current city name \n\nExample \n/set city Berlin \n\nIn this example, James will use Berlin as your current city.",
    "how_to_dailyupdate": "⚙️ *How To: /set dailyupdate* \n\nPlease use this format: /set dailyupdate `yes`/`no` \n\nParameters \n• Choose between yes/no, regarding if you wish James to send you an update every morning with weather and news informations \n\nExample \n/set dailyupdate yes \n\nIn this example, James will send you some useful informations every morning.",
    "set_city_success": "Success! ✅",
    "set_country_success": "Success! ✅",
    "set_daily_true_success": "Success! ✅ You will now get a daily update from me 🗞",
    "set_daily_false_success": "Success! ✅ You won't get any more daily updates.",
}

WEATHER = {
    "how_to": f"⚙️ *How To: /weather* \n\nPlease use this format: /weather `your_city` \n\nParameters \n• For `your_city` paste your current city name \n\nExample \n/weather Berlin \n\nIn this example, James will inform you about the weather in Berlin. \n\n_Hint: Use_ `/set city your-city-name`, _so that you don't need to specify your city in future._",
    "hint": "\n_Hint: Use_ `/set city your-city-name`, _so that you don't need to specify your city in future._",
    "city_not_found": "🤷‍♂️ Sorry, I couldn't find your city. Please try again.\n"
}