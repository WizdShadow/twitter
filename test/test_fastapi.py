#test_fastapi.py
from starlette.testclient import TestClient
from dotenv import load_dotenv
from httpx import AsyncClient
from main import app
import pytest
from confest import init_models, data_test, client, event_loop, session
from database.models import Base, User, Followers, Following
from sqlalchemy.future import select
from sqlalchemy import text
import os




#~ Тест на вывод информации о пользователе
@pytest.mark.asyncio
async def test_me_info(init_models, data_test, client, event_loop):
    headers = {"Api-Key": "test"}
    response = await client.get("/api/users/me", headers = headers)
    assert response.status_code == 200
        
    
#~ Тест на вывод информации о пользователе по id    
@pytest.mark.asyncio
async def test_id_info(init_models, data_test, client, event_loop):
    response = await client.get("/api/users/6")
    assert response.status_code == 200
    
    
#~ Тест на подписку пользователя
@pytest.mark.asyncio
async def test_sub(init_models, data_test, client, event_loop):
    headers = {"Api-Key": "test"}
    response = await client.post("/api/users/6/follow", headers = headers)
    assert response.status_code == 200

#~ Тест на подписку пользователя
@pytest.mark.asyncio
async def test_unsub(init_models, data_test, client, event_loop):
    headers = {"Api-Key": "test"}
    response = await client.delete("/api/users/6/follow", headers = headers)
    assert response.status_code == 200
    
# #~ Тест на создание твита
@pytest.mark.asyncio
async def test_create(init_models, data_test, client, event_loop):
    headers = {"Api-Key": "test"}
    body = {"id": 1,
            "content": "test",
            "attachments": [1]}
    response = await client.post("/api/tweets", headers = headers, json = body)
    assert response.status_code == 200
    
#~ Тест на лайкв твита
@pytest.mark.asyncio
async def test_like(init_models, data_test, client, event_loop):
    headers = {"Api-Key": "test"}
    response = await client.post("/api/tweets/1/like", headers = headers)
    assert response.status_code == 200
    assert response.json()["result"] == True
#~ Тест на удаление лайка
@pytest.mark.asyncio
async def test_unlike(init_models, data_test, client, event_loop):
    headers = {"Api-Key": "test"}
    response = await client.delete("/api/tweets/1/like", headers = headers)
    assert response.status_code == 200
    
    
#~ Тест на получение всех твитов
@pytest.mark.asyncio
async def test_all_tweets(init_models, data_test, client, event_loop):
    response = await client.get("/api/tweets")
    print(response.json())
    assert response.status_code == 200
    
#~ Тест на удаление твита
@pytest.mark.asyncio
async def test_delete_tweets(init_models, data_test, client, event_loop):
    headers = {"Api-Key": "test"}
    response = await client.delete("/api/tweets/1", headers = headers)
    assert response.status_code == 200
    assert response.json()["result"] == True
    