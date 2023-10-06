from services import news_service
from telegram import Update
from telegram.ext import ContextTypes


async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req_response = await news_service.get_news()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=req_response, parse_mode='Markdown', disable_web_page_preview=True)