import requests
from telegram import Update
from telegram.ext import ContextTypes
from decouple import config

NEWS_API_TOKEN = config('NEWS_API_TOKEN')
COUNTRY = 'de'

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await get_news_from_api()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode='Markdown', disable_web_page_preview=True)

async def get_news_from_api():
    url = f'https://newsapi.org/v2/top-headlines?country={COUNTRY}&apiKey={NEWS_API_TOKEN}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        response_text = f"📰 *News* • _Germany_\n\n"
        i = 0
        for i in range(5):
            response_text += f"👉🏼 [{data['articles'][i]['title']}]({data['articles'][i]['url']})\n\n"

    else:
        response_text = "😬 Sorry! There is an internal error. Please try again or contact the admin."

    return response_text

