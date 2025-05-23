import asyncio
import logging

from aiogram import  Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest

from DataBase.models import create_table
from Handlers import router
from config import bot_token


async def main():
    # Бот и подключение к Токен
    bot = Bot(token=bot_token)
    # Основной диспетчер для выполнения команд
    dp = Dispatcher()
    # Подключение Роутера
    dp.include_router(router)

    # Команда для исключений прежних обработок
    await bot.delete_webhook(drop_pending_updates=True)
    # Старт бота
    await dp.start_polling(bot)

# Точка Входа
if __name__ == '__main__':
    # Логирование процессов
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(create_table())
        asyncio.run(main())
    except TelegramBadRequest:
        print('Ошибка')
    except KeyboardInterrupt:
        print('Выход')
