import requests
from services import setting_service
from telegram import Update
from telegram.ext import ContextTypes
from decouple import config

NEWS_API_TOKEN = config('NEWS_API_TOKEN')
# COUNTRY = 'de'

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Hole User Settings und finde Land
    user_setting = await setting_service.get_setting_by_chat_id(update.effective_chat.id)
    if user_setting is not None:
        user_country = user_setting.get('country', setting_service.DEFAULT_COUNTRY)
        if user_country == 'ger': user_country = 'de'
    else:
        user_country = setting_service.DEFAULT_COUNTRY

    response = await get_news_from_api(user_country)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode='Markdown', disable_web_page_preview=True)

async def get_news_from_api(country):
    url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={NEWS_API_TOKEN}'
    response = requests.get(url)

    if country == 'de':
        country_string = 'Deutschland'
    else:
        country_string = 'USA'

    if response.status_code == 200:
        data = response.json()
        response_text = f"📰 *News* • _{country_string}_\n\n"
        i = 0
        for i in range(5):
            response_text += f"👉🏼 [{data['articles'][i]['title']}]({data['articles'][i]['url']})\n\n"

    else:
        response_text = "😬 Sorry! There is an internal error. Please try again or contact the admin."

    return response_text

