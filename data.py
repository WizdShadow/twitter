from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
import random
import asyncio
from database.models import User, Followers, Following, init_models, Base, engine
import time

async def init_models():
    async with engine.begin() as conn:
        # Сначала удаляем таблицы, если они существуют
        await conn.run_sync(Base.metadata.drop_all)
    print("модели созданы")

async def main():
    await init_models()
    # Дополнительный код для работы с базой данных

# Запуск асинхронного event loop
asyncio.run(main())