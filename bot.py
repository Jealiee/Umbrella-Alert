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

from geocode import get_coordinates
from weather import get_weather 
from logic import analyze_weather
from users import add_user, load_users

BOT_TOKEN = os.getenv("BOT_TOKEN")
user_seen = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Umbrella Alert! Send your city name to subscribe."
    )

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    city = update.message.text.strip()
    users = load_users()
    
    if len(city) < 3 or len(city) > 50 or not city.replace(" ", "").isalpha():
        await update.message.reply_text('Please send a valid city name (letters only).')
        return

    latitude, longitude = get_coordinates(city)
    if latitude is None or longitude is None:
        await update.message.reply_text("City not found. Please try another one")
        return 
    
    if any(u["chat_id"] == chat_id for u in users):
        await update.message.reply_text("You're already subscribed.")
        return
        

    add_user(chat_id, city, latitude, longitude)
    
    await update.message.reply_text(f'Got it! You will now recieve weather updates for {city}, every morning at 6am.')


def bot():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN variable not set.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    job_queue = app.job_queue
    job_queue.run_daily(send_updates, time=time(hour=6, minute=0, tzinfo = ZoneInfo("UTC")))
    app.run_polling()

async def send_updates(context: ContextTypes.DEFAULT_TYPE):
    users = load_users()

    for user in users:
        chat_id =  user["chat_id"]
        latitude = user["latitude"]
        longitude = user["longitude"]

        weather_data = get_weather(latitude, longitude)
        final_message = analyze_weather(weather_data)

        await context.bot.send_message( chat_id=chat_id,  text=final_message)
           
          
