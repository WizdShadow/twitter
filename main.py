from fastapi import FastAPI, Form, UploadFile, Depends, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database.models import User, Followers, Following, get_session, Medias, init_models, engine, Tweets, Likes, Base, async_session
from pydantic import BaseModel, ConfigDict
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import and_
from function.function_out import get_follower_following, get, post_like, get_user, get_name
from contextlib import asynccontextmanager
from typing import List
from shema import Tweetss, MediasOut, Status, InfoUser, Tweetsall, Tweetcreate
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_models()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)    


class GoodOut(BaseModel):
    result: bool = True

    model_config = ConfigDict(from_attributes=True) 
        

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request})

@app.middleware("http")
async def check_user_middleware(request: Request, call_next):
    if request.url.path.startswith("/api") and not request.url.path.startswith(
            "/api/medias/"
    ):
        async with async_session() as session:
            user = await get_user(
                session=session, api_key=request.headers.get("Api-Key", 'test') 
            )
            if not user:
                return Response(content="Unauthorized", status_code=401)

    return await call_next(request)


#~ Получение информации о пользователе
@app.get("/api/users/me")
async def user_me(request: Request, session = Depends(get_session)):
    key = request.headers.get("Api-Key")
    query = select(User).options(
        joinedload(User.followers),
        joinedload(User.following)
    ).where(User.name == key)
    
    result = await session.execute(query)
    
    user = result.unique().scalars().first()
    
    followers, followings = await get_follower_following(session, user.followers, user.following)
        
    return InfoUser(id = user.id, name = user.name, follower = followers, following = followings)

#~ Получение информации о пользователе по id
@app.get("/api/users/{id}")
async def user_me(id: int, session = Depends(get_session)):
    
    query = select(User).options(
        joinedload(User.followers),
        joinedload(User.following)
    ).where(User.id == id)
    
    result = await session.execute(query)
    
    user = result.unique().scalars().first()
    
    followers, followings = await get_follower_following(session, user.followers, user.following)
    if not user:
        return Status(result = False)
    return InfoUser(id = user.id, name = user.name, follower = followers, following = followings)
    
#~ Подписка на пользователя
@app.post("/api/users/{id}/follow")
async def user_follow(id: int, request: Request, session = Depends(get_session)):
    key = request.headers.get("Api-Key")
    id_user = await get_name(session, key)
    query = select(Following).where(and_(Following.user_id == id_user, Following.following_id == id))
    result = await session.execute(query)
    following = result.scalars().first()

    if following:
        return Status(result = False)

    else:
        add = Following(user_id=id_user, following_id=id)
        session.add(add)
        await session.commit()
        return Status(result = True)
        
#~ Отписка от пользователя
@app.delete("/api/users/{id}/follow")
async def user_follow(id: int, session = Depends(get_session)):
    user = 5
    user_following = 7

    query = select(Following).where(and_(Following.user_id == user, Following.following_id == user_following))
    result = await session.execute(query)
    following = result.scalars().first()

    if following:
        await session.delete(following)
        await session.commit()
        return Status(result = True)

    else:
        return Status(result = False)
            
#~ Загрузка картинок на сервер
@app.post("/api/medias")
async def create_media(file: UploadFile, session = Depends(get_session)):
    file_body = await file.read()
    media = await create_medias(file_body, session, file.filename)
    return MediasOut(media_id=media.id)
    
async def create_medias(file_body, session, file_name):
    file =  Medias(file_body=file_body, file_name=file_name)
    session.add(file)    
    await session.commit()
    return file

#~ Cоздать твит
@app.post("/api/tweets")
async def create_tweet(twet: Tweetss, request: Request, session = Depends(get_session)):
    key = request.headers.get("Api-Key")
    id_user = await get_name(session, key)
    query = select(Medias).where(Medias.id.in_(twet.attachments))
    result = await session.execute(query)
    attachments = result.scalars().all()
    
    for attachment in attachments:
        if attachment.tweet_id is not None:
            return Status(result = False)
    
    twets = (Tweets(content=twet.content, author_id=id_user))
    
    session.add(twets)
    await session.commit()
    
    for attachment in attachments:
        attachment.tweet_id = twets.id
    await session.commit()
        
    return Tweetcreate(result = True, id = twets.id)
  
#~ Удалить твит    
@app.delete("/api/tweets/{id}")
async def delete_tweets(id: int, request: Request, session = Depends(get_session)):
    key = request.headers.get("Api-Key")
    id_user = await get_name(session, key)
    query = select(Tweets).where(Tweets.id == id)
    result = await session.execute(query)    
    tweet = result.scalars().first()
    
    if tweet.author_id ==id_user:
        await session.delete(tweet)
        await session.commit()
        return Status(result = True)
    else:
        return Status(result = False)
    
#~ Поставить лайк
@app.post("/api/tweets/{id}/like")
async def like_tweets(id: int, request: Request, session = Depends(get_session)):
    key = request.headers.get("Api-Key")
    id_user = await get_name(session, key)
    query = select(Tweets).where(Tweets.id == id)
    result = await session.execute(query)    
    tweet = result.scalars().first()
    if tweet:
        returnn = await post_like(session, id, id_user)
        return Status(result = returnn)
        
    else:
        return Status(result = False)
    
    
#~ Удалить лайк
@app.delete("/api/tweets/{id}/like")
async def delete_like(id: int, request: Request, session = Depends(get_session)):
    key = request.headers.get("Api-Key")
    id_user = await get_name(session, key)
    query = select(Likes).where(and_(Likes.user_id == id_user, Likes.tweet_id == id))
    result = await session.execute(query)    
    like = result.scalars().first()
    if like:
        await session.delete(like)
        await session.commit()
        return Status(result = True)
    else:
        return Status(result = False)
    
#~ Получение всех твитов
@app.get("/api/tweets")
async def get_all_tweets(session = Depends(get_session)):
    query = select(Tweets).options(joinedload(Tweets.author),
                                   selectinload(Tweets.likes).joinedload(Likes.user),
                                   joinedload(Tweets.attachments).load_only(Medias.id))
    result = await session.execute(query)
    unique_result = result.unique()  
    tweets = unique_result.scalars().all()
    api = await get(tweets)
    return Tweetsall(result = True, tweets = api)

#~ Получение картинки
@app.get("/api/medeia/{id}")
async def get_media(id: int, session = Depends(get_session)):
    query = select(Medias).where(Medias.id == id)
    result = await session.execute(query)
    media = result.scalars().first()
    return Response(content=media.file_body, media_type=media.file_name)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)