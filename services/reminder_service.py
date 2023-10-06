import time, json, logging
from services import messagetext_service
from datetime import datetime

REMINDERS_LIST = 'reminders.json'

# SET REMINDER
async def set_reminder(chat_id, time_str, text):
    # Mapping der Zeiteinheiten
    time_units = {"m": 60, "h": 3600, "d": 86400, "w": 604800}

    # Check der Zeiteinheit
    unit = time_str[-1]
    if unit not in time_units:
        return messagetext_service.REMINDER['invalid_time_unit'], None

    # Check des Zeitwerts
    try:
        duration = int(time_str[:-1]) * time_units[unit]
    except ValueError:
        return messagetext_service.REMINDER['invalid_time_value'], None

    # Reminder erstellen und speichern
    try:
        reminder_id = int(time.time())
        new_reminder = {
            "reminder_id": reminder_id,
            "chat_id": chat_id,
            "reminder_time": int(time.time()) + duration,
            "reminder_text": text
        }
        await _save_reminder(new_reminder)
    except Exception as e:
        logging.error(str(e))
        return messagetext_service.GENERAL['error'], None

    return messagetext_service.REMINDER['success_new_reminder'], reminder_id

# CANCEL REMINDER
async def cancel_reminder(chat_id, reminder_id):
    removed = False
    try:
        reminders = await _get_all_reminders()
        for reminder in reminders:
            if reminder['chat_id'] == chat_id and int(reminder['reminder_id']) == int(reminder_id):
                reminders.remove(reminder)
                await _update_reminders_list(reminders)
                removed = True

        if removed:
            return messagetext_service.REMINDER['success_reminder_removed']
        else:
            return messagetext_service.REMINDER['reminder_not_found']

    except Exception as e:
        logging.error(str(e))
        return messagetext_service.GENERAL['error']

# LIST REMINDERS
async def list_reminders(chat_id):
    reminders_text = "_Timezone is UTC_\n\n"
    reminder_found = False
    reminders = await _get_all_reminders()

    for reminder in reminders:
        if reminder['chat_id'] == chat_id:
            dt_object = datetime.fromtimestamp(reminder['reminder_time']) # Zeit umwandeln
            formatted_date_time = dt_object.strftime("%d.%m.%y at %H:%M")
            reminders_text += f"📌 '{reminder['reminder_text']}' ({formatted_date_time})\n"
            reminder_found = True

    if reminder_found:
        return reminders_text
    else:
        return messagetext_service.REMINDER['empty_reminder_list']


#                    #
#  HELPER FUNCTIONS  #
#                    #
async def _save_reminder(new_reminder):
    try:
        reminders = await _get_all_reminders()
        reminders.append(new_reminder)
        await _update_reminders_list(reminders)
    except Exception as e:
        logging.error(str(e))

async def _get_all_reminders():
    try:
        with open(REMINDERS_LIST, 'r') as file:
            reminders = json.load(file)
    except FileNotFoundError:
        reminders = []
    return reminders

async def _update_reminders_list(new_reminders_list):
    try:
        with open(REMINDERS_LIST, 'w') as file:
            json.dump(new_reminders_list, file, indent=2)
    except Exception as e:
        logging.error(str(e))
