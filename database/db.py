"""
Модуль работы с SQLite.
Здесь создаётся таблица tasks и функции для добавления и чтения задач.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

# Файл базы лежит в корне проекта
DB_PATH = Path(__file__).resolve().parent.parent / "tasks.db"


def get_connection() -> sqlite3.Connection:
    """Открывает соединение с базой (row_factory — доступ к колонкам по имени)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Создаёт таблицу tasks, если её ещё нет."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                user TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def add_task(text: str, user: str) -> int:
    """
    Добавляет задачу в базу.
    Возвращает id новой записи.
    """
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (text, user, created_at) VALUES (?, ?, ?)",
            (text.strip(), user, created_at),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_tasks() -> list[sqlite3.Row]:
    """Возвращает все задачи, отсортированные по дате создания."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, text, user, created_at FROM tasks ORDER BY id ASC"
        )
        return cursor.fetchall()
