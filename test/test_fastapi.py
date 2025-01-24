#test_fastapi.py
from starlette.testclient import TestClient
from dotenv import load_dotenv
from httpx import AsyncClient
from main import app
import pytest
from confest import init_models, data_test, client
from database.models import Base, User, Followers, Following
from sqlalchemy.future import select
from sqlalchemy import text
import os




#~ Тест на вывод информации о пользователе
@pytest.mark.asyncio
def test_me_info(init_models, data_test, client):
    headers = {"Api-Key": "test"}
    response = client.get("/api/users/me", headers = headers)
    assert response.status_code == 200
        
    
    

def test_id_info(init_models, data_test, client):
    response = client.get("/api/users/6")
    assert response.status_code == 200
    
