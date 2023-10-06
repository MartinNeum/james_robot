from services import messagetext_service, weather_service
from telegram import Update
from telegram.ext import ContextTypes

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    incoming_command = context.args[0] if context.args else None