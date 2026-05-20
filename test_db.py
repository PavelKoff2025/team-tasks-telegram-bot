"""
Проверка работы базы данных без запуска Telegram-бота.
Запуск: python test_db.py
"""

from database.db import add_task, get_all_tasks, init_db


def main() -> None:
    print("Инициализация базы...")
    init_db()

    print("Добавление тестовой задачи...")
    task_id = add_task("Тестовая задача из test_db.py", "@test_user")
    print(f"  Создана задача с id = {task_id}")

    print("\nВсе задачи в базе:")
    tasks = get_all_tasks()
    if not tasks:
        print("  (пусто)")
    for row in tasks:
        print(f"  #{row['id']} | {row['created_at']} | {row['user']} | {row['text']}")

    print(f"\nИтого записей: {len(tasks)}")
    print("Проверка завершена успешно.")


if __name__ == "__main__":
    main()
