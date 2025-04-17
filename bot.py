from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from datetime import datetime
import asyncio
import os

# Получаем токен и чат ID из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Проверяем, что переменные окружения заданы
if not TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN и CHAT_ID должны быть заданы в переменных окружения")

DMB_DATE = datetime(2025, 6, 25)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['dembel'])
async def dmb_command(message: types.Message):
    days_left = (DMB_DATE - datetime.now()).days
    await message.reply(f"Кирюхе до дембеля осталось {days_left} дней")

async def daily_message():
    while True:
        now = datetime.now()
        if now.hour == 9 and now.minute == 0:
            days_left = (DMB_DATE - now).days
            await bot.send_message(chat_id=CHAT_ID, text=f"Доброе утро! До дембеля Кирюхи осталось {days_left} дней 💪")
            await asyncio.sleep(60)
        await asyncio.sleep(30)

async def on_startup(dp):
    asyncio.create_task(daily_message())

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
