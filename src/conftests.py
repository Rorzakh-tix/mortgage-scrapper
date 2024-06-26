import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from library.database.database_config import create_db_settings
from library.database.database import async_session_maker
from library.database.base_model import Base
from main import app


settings = create_db_settings()

engine_test = create_async_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
    poolclass=NullPool,
)

async_session_maker_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker_test() as session:
        yield session
