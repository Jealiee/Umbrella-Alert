import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from geocode import get_coordinates
from weather import get_weather 
from logic import analyze_weather

BOT_TOKEN = os.getenv("BOT_TOKEN")
user_seen = set()


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    city = update.message.text.strip()

    if chat_id not in user_seen:
        user_seen.add(chat_id)
        await update.message.reply_text(
            "Welcome to Umbrella Alert! Send your city name in chat to get started."
        )
        return
    
    if len(city) < 3 or len(city) > 50 or not city.replace(" ", "").isalpha():
        await update.message.reply_text('Please send a valid city name (letters only).')
        return

    latitude, longitude = get_coordinates(city)
    if latitude in None or longitude in None:
        await update.message.reply_text("City not found. Please try another one")
        return 

    weather_data = get_weather(latitude, longitude)
    final_message = analyze_weather(weather_data)
    await update.message.reply_text(final_message)


def bot():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN variable not set.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    app.run_polling()
