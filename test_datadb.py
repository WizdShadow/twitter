from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from faker import Faker
from sqlalchemy.orm import sessionmaker
from database.models import User, Followers, Following,  get_session, Medias, init_models, engine, Tweets, Likes
from sqlalchemy import select, and_
import random
import asyncio
import aiofiles
from PIL import Image
from test import get_id

engine = create_async_engine("postgresql+asyncpg://postgres:mysecretpassword@localhost:5400/twitter_test")
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



async def data_test():
    faker = Faker("en_US")
    async with AsyncSessionLocal() as session:
        test = User(name="test")
        session.add(test)
        await session.commit()
        # Добавляем пользователей
        for _ in range(10):
            user = User(name=faker.first_name())
            session.add(user)
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
        
        async with aiofiles.open("test/rengoku.jpg", mode='rb') as f:
            binary_data = await f.read()
                
        for _ in range(5):
            image = Medias(file_body=binary_data, file_name="test")
            session.add(image)
        await session.commit()
        
        
        twet_id = Tweets(content="test", author_id=1)
        session.add(twet_id)
        await session.commit()
        like = Likes(user_id=1, tweet_id=1)
        images = await get_id([2,3], session)
        for i in images:
            i.tweet_id = twet_id.id
        session.add(twet_id)
        session.add(like)
        await session.commit()
        
asyncio.run(data_test())