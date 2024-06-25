import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import create_db_settings
from database.base import async_session_maker
from database.models.base_model import Base
from main import app

settings = create_db_settings()

engine_test = create_async_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
    poolclass=NullPool,
)

async_session_maker_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="function")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_async_session():
    async with async_session_maker_test() as session:
        yield session

app.dependency_overrides[async_session_maker] = override_get_async_session


async def create_tables():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        yield


@pytest.fixture(scope='function')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
