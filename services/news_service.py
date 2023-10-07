import requests
from services import setting_service
from telegram import Update
from telegram.ext import ContextTypes
from decouple import config

NEWS_API_TOKEN = config('NEWS_API_TOKEN')
COUNTRY = 'de'

async def get_news():
    url = f'https://newsapi.org/v2/top-headlines?country={COUNTRY}&apiKey={NEWS_API_TOKEN}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        text = "📰 *News* • _Germany_\n\n"
        i = 0
        for i in range(5):
            text += f"👉🏼 [{data['articles'][i]['title']}]({data['articles'][i]['url']})\n\n"

        return text
