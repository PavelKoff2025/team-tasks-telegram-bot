"""
Точка входа: запуск Telegram-бота.
Запуск: python main.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import setup_routers
from database.db import init_db

# Логи в консоль — удобно при отладке
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # Создаём таблицу в SQLite при старте
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем обработчики команд
    dp.include_router(setup_routers())

    logging.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
