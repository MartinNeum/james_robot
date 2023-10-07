from services import messagetext_service, setting_service
from telegram import Update
from telegram.ext import ContextTypes

# {incomming_command: object field}
setting_commands = {
    "city": "city",
    "dailyupdate": "get_daily"
}

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    incomming_endpoint = update.message.text.split()[0]
    incoming_command = context.args[0] if context.args else None
    chat_id = update.effective_chat.id

    # Check user setting
    setting = await setting_service.get_user_setting(chat_id)
    if setting is None:
        setting = await setting_service.initialize_user_setting(chat_id, update.effective_user.first_name)

    # Handle /settings
    if incomming_endpoint == '/settings':
        daily = "Yes" if setting['get_daily'] else "No"
        text = f"⚙️ *Settings*\n\n"
        text += f"• Name: {setting['username']} \n• City: {setting['city']} \n• Daily update: {daily}"
        req_response = text

    # Handle /set
    elif incomming_endpoint == '/set':
        if incoming_command is None:
            req_response = messagetext_service.SETTING['how_to']
        
        elif incoming_command.lower() == 'city':
            if len(context.args) != 2:
                req_response = messagetext_service.SETTING['how_to_city']
            else:
                req_response = await setting_service.update_setting(chat_id, setting_commands['city'], context.args[1])
        elif incoming_command.lower() == 'dailyupdate':
            if len(context.args) != 2:
                req_response = messagetext_service.SETTING['how_to_dailyupdate']
            else:
                val = True if context.args[1] == 'yes' else False
                req_response = await setting_service.update_setting(chat_id, setting_commands['dailyupdate'], val)
        else:
            req_response = "How To"

    else:
        req_response = messagetext_service.SETTING['how_to']

    await context.bot.send_message(chat_id=chat_id, text=req_response, parse_mode='Markdown')