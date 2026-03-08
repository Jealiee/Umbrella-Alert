import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from datetime import time
from zoneinfo import ZoneInfo

from geocode import get_coordinates, get_timezone
from weather import get_weather
from logic import analyze_weather
from users import add_user, load_users, update_user

BOT_TOKEN = os.getenv("BOT_TOKEN")
user_seen = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Umbrella Alert! Send your city name to subscribe."
    )


async def set_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    users = load_users()

    if not context.args:
        await update.message.reply_text("Usage: /city Berlin")
        return

    city = " ".join(context.args)

    if len(city) < 3 or len(city) > 50 or not city.replace(" ", "").isalpha():
        await update.message.reply_text("Please send a valid city name (letters only).")
        return

    latitude, longitude = get_coordinates(city)
    if latitude is None or longitude is None:
        await update.message.reply_text("City not found. Please try another one")
        return

    timezone = get_timezone(latitude, longitude)
    if timezone is None:
        await update.message.reply_text("Could not determine timezone. Please try another city.")
        return

    existing_user = next((u for u in users if u["chat_id"] == chat_id), None)

    if existing_user:
        update_user(chat_id, city, latitude, longitude, timezone)
        await update.message.reply_text(f"Your city has been updated to {city}.")
    else:
        add_user(chat_id, city, latitude, longitude, timezone)
        await update.message.reply_text(
            f"Got it! You will now receive weather updates for {city} every morning at 6:00 your local time."
        )


async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sorry. Umbrella Alert does not accept messages. To change your city type: /city city_name"
    )


async def send_updates(context: ContextTypes.DEFAULT_TYPE):
    users = load_users()

    for user in users:
        chat_id = user["chat_id"]
        latitude = user["latitude"]
        longitude = user["longitude"]

        try:
            weather_data = get_weather(latitude, longitude)
            final_message = analyze_weather(weather_data)
            await context.bot.send_message(chat_id=chat_id, text=final_message)

        except Exception as e:
            print(f"Failed to send update to {chat_id}: {e}")


def bot():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN variable not set.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("city", set_city))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reject))

    job_queue = app.job_queue
    users = load_users()
    for user in users:
        job_queue.run_daily(
            send_updates, 
            time=time(hour=6, minute=0, tzinfo=ZoneInfo(user['timezone'])),
            context=user["chat_id"]
        )
    app.run_polling()
