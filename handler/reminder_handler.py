from services import messagetext_service, reminder_service
from telegram import Update
from telegram.ext import ContextTypes

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_reminder_id = None
    incoming_command = context.args[0] if context.args else None

    if incoming_command is None:
        req_response = messagetext_service.REMINDER['how_to']

    # Handle SET
    elif incoming_command.lower() == 'set':
        if len(context.args) < 3:
            req_response = messagetext_service.REMINDER['how_to_set']

        else:
            time_str = context.args[1] if context.args[1] else None
            text = " ".join(context.args[2:])

            if not time_str or not text:
                req_response = messagetext_service.REMINDER['how_to_set']
            else:
                req_response, new_reminder_id = await reminder_service.set_reminder(update.effective_chat.id, time_str, text)

    # Handle CANCEL
    elif incoming_command.lower() == 'cancel':
        if len(context.args) != 2:
            req_response = messagetext_service.REMINDER['how_to_cancel']

        else:
            remove_reminder_id = context.args[1] if context.args[1] else None
            req_response = await reminder_service.cancel_reminder(update.effective_chat.id, remove_reminder_id)

    # Handle LIST
    elif incoming_command.lower() == 'list':
        req_response = await reminder_service.list_reminders(update.effective_chat.id)

    # Handle Unbekannt
    else:
        req_response = messagetext_service.REMINDER['how_to']

    await context.bot.send_message(chat_id=update.effective_chat.id, text=req_response, parse_mode='Markdown')
    if new_reminder_id is not None: await context.bot.send_message(chat_id=update.effective_chat.id, text=new_reminder_id, parse_mode='Markdown')