from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, select, create_engine
from database.models import Base, User, Followers, Following
import pytest
import pytest_asyncio
from faker import Faker
import random
from starlette.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from main import app
import os
from dotenv import load_dotenv

engines = create_engine(os.getenv("DATABASE_URL_TEST_SYNC"))
async_session = sessionmaker(engines)

load_dotenv()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
        
        
@pytest.fixture(scope="session")
def init_models():
    engine = create_engine(os.getenv("DATABASE_URL_TEST_SYNC"))
    session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    
    yield session
    
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="session")
def data_test():
    faker = Faker("en_US")
    with async_session() as session:
        # Добавляем пользователей
        for _ in range(10):
            user = User(name=faker.first_name())
            session.add(user)
        session.commit()

        test = User(name="test")
        session.add(test)
        session.commit()

        # Получаем список всех пользователей
        result = session.execute(select(User))
        users = result.scalars().all()
        user_ids = [user.id for user in users]

        # Добавляем подписчиков и подписки
        for _ in range(10):
            while True:
                follower_id = random.choice(user_ids)
                following_id = random.choice(user_ids)
                dubl = session.execute(
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

        session.commit()

        yield  # Тестовые данные готовы

        # Очистка данных после теста
        session.execute(Followers.__table__.delete())
        session.execute(Following.__table__.delete())
        session.execute(User.__table__.delete())
        session.commit()