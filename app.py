"""Точка входа начиная с 3-й лекции"""
import asyncio
from os import getenv  # Переделал под pycharm в виртуальное окружение

from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties

from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession

from database.engine import create_db, drop_db, session_maker

from handlers.user_group import user_group_router
from handlers.user_private import user_private_router
from handlers.admin_private import admin_router


bot = Bot(token=getenv('TOKEN'),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # Тоже редакция вместо os.getenv - сразу getenv
# bot = Bot(token=getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # Понадобится при смене версии на 3.5.0
# так же нужно будет импортировать этот метод прямо с aiogram , сейчас он тут from aiogram.client.bot import DefaultBotProperties
bot.my_admins_list = []

dp = Dispatcher()

# admin_router.message.middleware.outer_middleware(CounterMiddleware())

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())

## pip install sqlalchemy - работая через ORM "sqlalchemy" ваш код никак
# не будет привязан к конкретной базе данных: mariadb postgres mysql
# pip install aiosqlite - для работы с бд в асинхронном режиме
# pip install asyncpg - для работы с postgres бд
