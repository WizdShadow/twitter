from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, LargeBinary
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv



if os.getenv("ENV") == "test":
    database_url = os.getenv("DATABASE_URL_TEST")
else:
    database_url = os.getenv("DATABASE_URL")

# Теперь создаем движок
engine = create_async_engine(database_url)
Base = declarative_base()
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session():
    async with async_session() as session:
        yield session
        
async def init_models():
    if os.getenv("ENV") == "test":
        asyncc_engine = create_async_engine(os.getenv("DATABASE_URL_TEST"))
        async with asyncc_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)        
    else:
        asyncc_engine = create_async_engine(os.getenv("DATABASE_URL"))
        async with asyncc_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    
    followers = relationship(
        "Followers",
        primaryjoin="User.id == Followers.user_id",
        back_populates="user",
        lazy="select",
    )

    
    following = relationship(
        "Following",
        primaryjoin="User.id == Following.user_id",
        back_populates="user",
        lazy="select",
    )

    tweets = relationship(
        "Tweets",
        lazy="select",
        back_populates="author",
        cascade="all, delete-orphan"
    )
    
    likes = relationship(
        "Likes",
        lazy="select",
        back_populates="user",
        cascade="all, delete-orphan"
    )


#~ Кто подписан на пользователя
class Followers(Base):
    __tablename__ = 'follower'
    __table_args__ = (UniqueConstraint('user_id', 'follower_id'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Связь с таблицей User
    user = relationship(
        "User",
        foreign_keys=[user_id],  
        back_populates="followers",
    )

#~ На кого подписан
class Following(Base):
    __tablename__ = 'following'
    __table_args__ = (UniqueConstraint('user_id', 'following_id'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    
    user = relationship(
        "User",
        foreign_keys=[user_id],  
        back_populates="following",
    )


class Medias(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True)
    file_body = Column(LargeBinary)
    file_name = Column(String)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)
    
    tweet = relationship("Tweets", back_populates="attachments")
    
    
class Tweets(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", lazy="select", back_populates="tweets")
    
    attachments = relationship(
        "Medias", lazy="select", back_populates="tweet", cascade="all, delete-orphan"
    )
    likes = relationship(
        "Likes", lazy="select", back_populates="tweet", cascade="all, delete-orphan"
    )

class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    
    user = relationship("User", lazy="select", back_populates="likes")
    tweet = relationship("Tweets", lazy="select", back_populates="likes")