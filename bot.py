import telebot
import os
import time
from datetime import datetime

# Токен бота
API_TOKEN = os.getenv("7997057858:AAGeQc_0GaFfok0xN4BrbDr2QaDzYVgc_8s")
CHAT_ID = int(os.getenv("CHAT_ID"))
DMB_DATE = datetime(2025, 6, 25)

bot = telebot.TeleBot(API_TOKEN)

# Функция для расчета количества дней до дембеля
def days_until_demob():
    today = datetime.now()
    delta = DMB_DATE - today
    return delta.days

# Обработчик команды /dembel
@bot.message_handler(commands=["dembel"])
def handle_dmb_command(message):
    days_left = days_until_demob()
    bot.reply_to(message, f"До дембеля Кирюхи осталось {days_left} дней.")

# Отправка ежедневного сообщения
def send_daily_message():
    while True:
        now = datetime.now()
        if now.hour == 9 and now.minute == 0:
            days_left = days_until_demob()
            bot.send_message(CHAT_ID, f"Доброе утро! До дембеля Кирюхи осталось {days_left} дней 💪")
            time.sleep(60)  # Отправлять сообщение каждое утро в 9:00
        time.sleep(30)  # Проверять раз в 30 секунд

# Запуск бота
if __name__ == '__main__':
    # Запуск бота в отдельном потоке для обработки команд
    import threading
    threading.Thread(target=send_daily_message, daemon=True).start()

    # Запуск бота для обработки команд /dembel
    bot.polling(none_stop=True)
