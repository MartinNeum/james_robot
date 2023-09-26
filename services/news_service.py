import requests
from telegram import Update
from telegram.ext import ContextTypes
from decouple import config

NEWS_API_TOKEN = config('NEWS_API_TOKEN')
COUNTRY = 'de'

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    url = f'https://newsapi.org/v2/top-headlines?country={COUNTRY}&apiKey={NEWS_API_TOKEN}'
    response = requests.get(url)

    response_text = f"📰 *News*\n\n"

    if response.status_code == 200:
        data = response.json()

        i = 0
        for i in range(5):
            # print(f"{data['articles'][i]}\n")
            response_text += f"👉🏼 [{data['articles'][i]['title']}]({data['articles'][i]['url']})\n\n"

    else:
        response_text = "😬 Sorry! There is an internal error. Please try again or contact the admin."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text, parse_mode='Markdown')

