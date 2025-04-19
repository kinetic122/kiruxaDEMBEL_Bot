import os
import time
import requests
from datetime import datetime

# Можно либо указать прямо здесь, либо через os.environ
BOT_TOKEN = os.getenv("BOT_TOKEN", "твой_токен")
CHAT_ID = os.getenv("CHAT_ID", "твой_чат_id")
DMB_DATE = datetime(2025, 6, 25)

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(text):
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def handle_command(message_text):
    if "/dembel" in message_text:
        days_left = (DMB_DATE - datetime.now()).days
        send_message(f"Кирюхе до дембеля осталось {days_left} дней")

def run_bot():
    print("Бот запущен...")
    last_update_id = None
    sent_today = False

    while True:
        # Обработка команды
        updates = get_updates(offset=last_update_id)
        if updates["ok"] and updates["result"]:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    handle_command(update["message"]["text"])

        # Авто-сообщение утром
        now = datetime.now()
        if now.hour == 9 and not sent_today:
            days_left = (DMB_DATE - now).days
            send_message(f"Доброе утро! До дембеля Кирюхи осталось {days_left} дней 💪")
            sent_today = True
        if now.hour == 0:
            sent_today = False

        time.sleep(2)

if __name__ == "__main__":
    run_bot()
