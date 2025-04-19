import os
import time
import requests
import random
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN", "7997057858:AAGeQc_0GaFfok0xN4BrbDr2QaDzYVgc_8s")
CHAT_ID = os.getenv("CHAT_ID", "-1002632304229")
DMB_DATE = datetime(2025, 6, 25)
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
GAME_FILE = "game_days.txt"

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(text):
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def get_game_days():
    if not os.path.exists(GAME_FILE):
        with open(GAME_FILE, "w") as f:
            f.write("0")
        return 0
    with open(GAME_FILE, "r") as f:
        content = f.read().strip()
        if content.isdigit() or (content.startswith('-') and content[1:].isdigit()):
            return int(content)
        else:
            # Если файл повреждён или пустой — обнуляем
            with open(GAME_FILE, "w") as f:
                f.write("0")
            return 0


def update_game_days(change):
    current = get_game_days()
    new_value = current + change
    with open(GAME_FILE, "w") as f:
        f.write(str(new_value))
    return new_value

def handle_command(message_text):
    if "/dembel" in message_text and "GAME" not in message_text:
        days_left = (DMB_DATE - datetime.now()).days
        send_message(f"Кирюхе до дембеля осталось {days_left} дней")

    elif "/dembelGAME" in message_text:
        change = random.randint(-365, 365)
        total = update_game_days(change)
        if change > 0:
            msg = f"Упс! К дембелю добавлено {change} дней 😅\nОбщий игровой счётчик: {total} дней"
        elif change < 0:
            msg = f"Заебись! Дней до дембеля стало меньше на {abs(change)} 💥\nОбщий игровой счётчик: {total} дней"
        else:
            msg = f"Ничего не изменилось, баффов не завезли 🙃\nОбщий игровой счётчик: {total} дней"
        send_message(msg)

def run_bot():
    print("Бот запущен...")
    last_update_id = None
    sent_today = False

    while True:
        updates = get_updates(offset=last_update_id)
        if updates["ok"] and updates["result"]:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    handle_command(update["message"]["text"])

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
