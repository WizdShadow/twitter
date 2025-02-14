from sqlalchemy.future import select
from typing import List, Optional, Dict
from pydantic import BaseModel
from database import User, Followers, Following, get_session, Medias, init_models, engine, Tweets, Likes
from sqlalchemy.orm import joinedload, selectinload

class Author(BaseModel):
    id: int
    name: str

class Like(BaseModel):
    user_id: Optional[int]
    name: Optional[str]

class Attachment(BaseModel):
    id: int

class Tweet(BaseModel):
    id: int
    content: str
    attachments: Optional[List[Attachment]] = []  # attachments теперь может быть пустым
    author: Author
    likes: Optional[List[Like]] = None  # likes тоже может быть пустым

    def get_attachments_as_links(self) -> List[str]:
        """Преобразует список вложений в список ссылок."""
        return [f"api/media/{attachment.id}" for attachment in self.attachments] if self.attachments else []
    
    
class Tweetss(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int]
    
class MediasOut(BaseModel):
    media_id: int
    
class Status(BaseModel):
    result: bool
class Userss(BaseModel):
    id: int
    name: str
    followers: Optional[List]
    following: Optional[List]    

class InfoUser(BaseModel):
    result: bool
    user: Userss
    
class Tweetsall(BaseModel):
    result: bool
    tweets: List   
    
class Tweetcreate(BaseModel):
    result: bool
    id: int     
    
