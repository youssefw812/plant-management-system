import requests
import json
from datetime import datetime
plants = []
def load_plants():
    global plants
    try:
        with open("plants.json", "r", encoding="utf-8") as file:
            plants = json.load(file)

    except FileNotFoundError:
        plants = []

BOT_TOKEN = "#add your Bot Token"
CHAT_IDS=# add your ID From telegram

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": message
            }
    )

def get_alerts():
    alerts = []

    today = datetime.now().date()

    for plant in plants:

        last_watered = datetime.strptime(
            plant['last_watered'],
            "%Y-%m-%d"
        ).date()

        days_since_watered = (
            today - last_watered
        ).days

        if days_since_watered >= int(plant['watering_interval']):
            alerts.append(
                f"🔴 {plant['name']} يحتاج إلى سقاية"
            )

        last_fertilized = datetime.strptime(
            plant['fertilized'],
            "%Y-%m-%d"
        ).date()

        days_since_fertilized = (
            today - last_fertilized
        ).days

        if days_since_fertilized >= 30:
            alerts.append(
                f"🛑 {plant['name']} يحتاج إلى تسميد"
            )

    return alerts

def check_and_notify():

    alerts = get_alerts()

    if alerts:
        send_telegram_message(
            "\n".join(alerts)
        )
