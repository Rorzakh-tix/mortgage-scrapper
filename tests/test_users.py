import jwt
import pytest

from database.models.user_model import User
from tests.conftests import prepare_database, client, async_session_maker_test


async def test_register(prepare_database):
    user_data = {
        "email": "user@example.com",
        "password": "password123",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    }
    responce_data = await client.post("/auth/register", json=user_data)
    assert responce_data.status_code == 201
    data = responce_data.json()
    assert data["email"] == user_data["email"]
    async with async_session_maker_test() as session:
        db_user = await session.get(User, data["id"])
        assert db_user is not None
        assert db_user.email == user_data["email"]
        assert db_user.hashed_password != user_data["password"]


async def test_login(prepare_database):
    user_data = {
        "email": "user@example.com",
        "password": "password123",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    }
    responce_data = await client.post("/auth/register", json=user_data)
    assert responce_data.status_code == 201
    user_data = {
        "username": "user@example.com",
        "password": "password123",
    }
    responce_data = await client.post("/auth/jwt/login", data=user_data)
    assert responce_data.status_code == 200
    data = responce_data.json()
    async with async_session_maker_test() as session:
        decoded_token = jwt.decode(data["access_token"], "SECRET_PHRASE", algorithms=["HS256"],audience="fastapi-users:auth")
        userid_test = decoded_token['sub']
        print(decoded_token)
        db_user = await session.get(User, userid_test)
        assert userid_test == str(db_user.id)
