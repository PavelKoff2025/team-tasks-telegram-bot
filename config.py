"""
Настройки бота: токен из переменной окружения BOT_TOKEN.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Загружаем .env из корня проекта
load_dotenv(Path(__file__).resolve().parent / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError(
        "Не задан BOT_TOKEN. Создайте файл .env по образцу .env.example "
        "и укажите токен от @BotFather."
    )
