from database.models import User
from sqlalchemy.future import select
import json
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
    id: int
    content: str
    attachments: List[int]
    
class MediasOut(BaseModel):
    media_id: int
    
class Status(BaseModel):
    result: bool
    
class InfoUser(BaseModel):
    id: int
    name: str
    follower: List
    following: List
    
class Tweetsall(BaseModel):
    result: bool
    tweets: List   
    
class Tweetcreate(BaseModel):
    result: bool
    id: int     