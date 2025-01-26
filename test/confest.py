import os
import random
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_
from database.models import Base, User, Followers, Following
import pytest
import pytest_asyncio
from faker import Faker
from httpx import AsyncClient, ASGITransport
from main import app
import asyncio


load_dotenv()


async_engine = create_async_engine(os.getenv("DATABASE_URL_TEST_SYNC"))
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()  
    asyncio.set_event_loop(loop)     
    yield loop
    loop.close() 
    
    
# Фикстура для клиента
@pytest_asyncio.fixture(scope="session")
async def client(event_loop):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

# Фикстура для инициализации моделей
@pytest_asyncio.fixture(scope="session")
async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Фикстура для тестовых данных
@pytest_asyncio.fixture(scope="session")
async def data_test():
    faker = Faker("en_US")
    async with AsyncSessionLocal() as session:
        # Добавляем пользователей
        for _ in range(10):
            user = User(name=faker.first_name())
            session.add(user)
        await session.commit()

        test = User(name="test")
        session.add(test)
        await session.commit()

        # Получаем список всех пользователей
        result = await session.execute(select(User))
        users = result.scalars().all()
        user_ids = [user.id for user in users]

        # Добавляем подписчиков и подписки
        for _ in range(10):
            while True:
                follower_id = random.choice(user_ids)
                following_id = random.choice(user_ids)
                dubl = await session.execute(
                    select(Followers).where(
                        and_(Followers.user_id == following_id, Followers.follower_id == follower_id)
                    )
                )
                dubl = dubl.scalars().first()
                if follower_id != following_id and not dubl:
                    break

            # Создаем запись о подписчике
            follower = Followers(user_id=following_id, follower_id=follower_id)
            session.add(follower)

            # Создаем запись о подписке
            following = Following(user_id=follower_id, following_id=following_id)
            session.add(following)

        await session.commit()

        yield  # Тестовые данные готовы

        # Очистка данных после теста
        await session.execute(Followers.__table__.delete())
        await session.execute(Following.__table__.delete())
        await session.execute(User.__table__.delete())
        await session.commit()