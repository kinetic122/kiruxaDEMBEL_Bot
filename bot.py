import os
import time
import requests
from datetime import datetime
import random

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
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

def get_game_days():
    if not os.path.exists("game_days.txt"):
        with open("game_days.txt", "w") as f:
            f.write("0")
    with open("game_days.txt", "r") as f:
        content = f.read().strip()
        return int(content) if content else 0

def update_game_days(change):
    current = get_game_days()
    new_total = max(current + change, 0)
    with open("game_days.txt", "w") as f:
        f.write(str(new_total))
    return new_total

def weighted_random_change():
    if random.random() < 0.2:
        return 0  # 20% шанс, что ничего не поменяется

    weights = {
        range(1, 11): 70,
        range(11, 31): 20,
        range(31, 101): 5,
        range(101, 366): 1
    }
    ranges = list(weights.keys())
    chances = list(weights.values())
    chosen_range = random.choices(ranges, weights=chances)[0]
    value = random.choice(list(chosen_range))
    return random.choice([-1, 1]) * value

def handle_command(message_text):
    text = message_text.lower()

    if "/dembelgame" in text:
        change = weighted_random_change()
        current = get_game_days()
        if change < 0 and abs(change) > current:
            change = -current
        total = update_game_days(change)

        if change > 0:
            send_message(f"Упс! К дембелю добавлено {change} дней! 😂\nОсталось дней😂: {total}")
        elif change < 0:
            send_message(f"Заебись! Дней до дембеля стало меньше на {abs(change)} дней! 🔥\nОсталось дней😂: {total}")
        else:
            real_days = (DMB_DATE - datetime.now()).days + total
            send_message(f"Нихуя не поменялось, Кирюхе осталось {real_days} дней 👀")

    elif "/dembel" in text:
        days_left = (DMB_DATE - datetime.now()).days
        send_message(f"Кирюхе до дембеля осталось {days_left} дней")


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
