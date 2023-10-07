import logging, json
from services import messagetext_service

SETTINGS_LIST = 'settings.json'

async def update_setting(chat_id, setting_field, value):
    try:
        setting = await _get_setting_by_chat_id(chat_id)

        if setting is not None:
            setting[setting_field] = value
            success = await _update_setting(chat_id, setting)
            if not success:
                return messagetext_service.GENERAL['error']
        else:
            return messagetext_service.GENERAL['error']
        
        return messagetext_service.SETTING['set_city_success']
        
    except Exception as e:
        logging.error(str(e))
        return messagetext_service.GENERAL['error']
    
async def initialize_user_setting(chat_id, username):
    new_setting = {
        "chat_id": chat_id,
        "username": username,
        "language": None,
        "city": None,
        "country": None,
        "get_daily": False
    }

    return await _save_new_setting(new_setting)

async def get_user_setting(chat_id):
    return await _get_setting_by_chat_id(chat_id)

####################
# Helper functions #
####################
async def _save_new_setting(new_setting):
    try:
        settings = await _get_all_settings()
        settings.append(new_setting)
        await _update_settings_list(settings)
        return new_setting
    except Exception as e:
        logging.error(str(e))
        return None

async def _update_setting(chat_id, updated_setting):
    try:
        settings = await _get_all_settings()
        for setting in settings:
            if setting['chat_id'] == chat_id:
                settings.remove(setting)
                settings.append(updated_setting)
                await _update_settings_list(settings)
                return True
        return False
    except Exception as e:
        logging.error(str(e))

async def _get_setting_by_chat_id(chat_id):
    try:
        settings = await _get_all_settings()
        for setting in settings:
            if setting['chat_id'] == chat_id:
                return setting
        return None
    except Exception as e:
        logging.error(str(e))

async def _get_all_settings():
    try:
        with open(SETTINGS_LIST, 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = []
    return settings

async def _update_settings_list(new_settings_list):
    try:
        with open(SETTINGS_LIST, 'w') as file:
            json.dump(new_settings_list, file, indent=2)
    except Exception as e:
        logging.error(str(e))
