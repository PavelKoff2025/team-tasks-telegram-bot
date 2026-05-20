"""
Регистрация всех обработчиков команд в одном роутере.
"""

from aiogram import Router

from handlers.commands import router as commands_router


def setup_routers() -> Router:
    """Собирает роутеры из разных модулей в один главный."""
    main_router = Router()
    main_router.include_router(commands_router)
    return main_router
