# import os
from os import getenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base

#from .env file:
# DB_LITE=sqlite+aiosqlite:///my_base.db
# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name
# DB_URL=postgresql+asyncpg://bot:bot@localhost:5432/bot

# engine = create_async_engine(os.getenv('DB_LITE'), echo=True)

# engine = create_async_engine(getenv('DB_LITE'), echo=True)
engine = create_async_engine(getenv('DB_URL'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



# Функция создающая привязку к базе данных или просто базу данных асинхронно
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция удаляющая привязку к базе данных или просто базу данных асинхронно
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
