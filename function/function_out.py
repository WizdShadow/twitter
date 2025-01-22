from database.models import User
from sqlalchemy.future import select
import json
from typing import List, Optional, Dict
from pydantic import BaseModel
from database import User, Followers, Following, get_session, Medias, init_models, engine, Tweets, Likes
from sqlalchemy.orm import joinedload, selectinload
from shema.shema import Tweet
import uvicorn

async def get_follower_following(session, a,b):
    
    follower = []
    following = []
    
    for followerr in a:
        query = select(User).where(User.id == followerr.follower_id)
        result = await session.execute(query)
        fol = result.scalars().first()
        if fol:
            follower.append({"id": fol.id, "name": fol.name})

    for followingg in b:
        query = select(User).where(User.id == followingg.following_id)
        result = await session.execute(query)
        fols = result.scalars().first()
        if fols:
            print(fols.name)
            following.append({"id": fols.id, "name": fols.name})
            
    return follower, following

async def get(example_data):
    tweets = []

    for data in example_data:
        tweet_data = {
            'id': data.id,
            'content': data.content,
            'author': {
                'id': data.author.id,
                'name': data.author.name
            },
            'likes': [
                {'user_id': like.user.id, 'name': like.user.name} for like in data.likes
            ] if data.likes else [],
            'attachments': [
                {'id': attachment.id} for attachment in data.attachments
            ] if data.attachments else []
        }

        tweets.append(Tweet(**tweet_data))

    for tweet in tweets:
        tweet.attachments = tweet.get_attachments_as_links()

    serialized_tweets = tweets

    return serialized_tweets


async def post_like(session, id):
    us = 7
    queryy = select(Likes).where(Tweets.id == id)
    resultt = await session.execute(queryy)    
    like = resultt.scalars().first()
    if not like:
        likes = Likes(user_id=us, tweet_id=id)
        session.add(likes)
        await session.commit()
        return True
    else:
        likes = Likes(user_id=us, tweet_id=id)
        session.add(likes)
        await session.commit()
        return True

#~ Проверка юзеров наличие
async def get_user(session, api_key):
    query = select(User).where(User.name == api_key)
    result = await session.execute(query)
    user = result.scalars().first()
    
    return user
    
