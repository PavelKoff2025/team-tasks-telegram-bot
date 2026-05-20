"""
Обработчики команд: /start, /add, /list, /list_csv.
"""

import csv
import io
import tempfile
from pathlib import Path

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import FSInputFile, Message

from database.db import add_task, get_all_tasks

router = Router(name="commands")


def _format_user(message: Message) -> str:
    """Имя пользователя для поля user в базе (username или id)."""
    if message.from_user and message.from_user.username:
        return f"@{message.from_user.username}"
    if message.from_user:
        return str(message.from_user.id)
    return "unknown"


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Приветствие и краткая справка по командам."""
    await message.answer(
        "Привет! Я бот для общего списка задач команды.\n\n"
        "Команды:\n"
        "/add <текст> — добавить задачу\n"
        "/list — показать все задачи\n"
        "/list_csv — скачать список в CSV\n"
        "/start — это сообщение"
    )


@router.message(Command("add"))
async def cmd_add(message: Message, command: CommandObject) -> None:
    """
    Добавляет задачу.
    Пример: /add Купить кофе для офиса
    """
    # command.args — текст после команды /add
    task_text = (command.args or "").strip()

    if not task_text:
        await message.answer(
            "Укажите текст задачи после команды.\n"
            "Пример: /add Подготовить отчёт к пятнице"
        )
        return

    user = _format_user(message)
    task_id = add_task(task_text, user)

    await message.answer(f"Задача #{task_id} добавлена:\n{task_text}")


@router.message(Command("list"))
async def cmd_list(message: Message) -> None:
    """Выводит все задачи текстом в чат."""
    tasks = get_all_tasks()

    if not tasks:
        await message.answer("Список задач пуст. Добавьте первую: /add ...")
        return

    lines = ["Общий список задач:\n"]
    for row in tasks:
        lines.append(
            f"#{row['id']} | {row['created_at']}\n"
            f"Автор: {row['user']}\n"
            f"{row['text']}\n"
        )

    # Telegram ограничивает длину сообщения (~4096 символов)
    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:4000] + "\n\n... (список обрезан, используйте /list_csv)"

    await message.answer(text)


@router.message(Command("list_csv"))
async def cmd_list_csv(message: Message) -> None:
    """Формирует CSV-файл и отправляет его пользователю."""
    tasks = get_all_tasks()

    if not tasks:
        await message.answer("Нет задач для экспорта.")
        return

    # Пишем CSV в память (строковый буфер)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["id", "text", "user", "created_at"])

    for row in tasks:
        writer.writerow([row["id"], row["text"], row["user"], row["created_at"]])

    # Сохраняем во временный файл — так удобнее отправить документ в Telegram
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
        newline="",
    ) as tmp:
        tmp.write(buffer.getvalue())
        tmp_path = Path(tmp.name)

    try:
        document = FSInputFile(tmp_path, filename="tasks.csv")
        await message.answer_document(
            document=document,
            caption=f"Экспорт задач: {len(tasks)} шт.",
        )
    finally:
        # Удаляем временный файл после отправки
        tmp_path.unlink(missing_ok=True)
