from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from src.database.models.base_model import Base
# from src.config import settings

# DATABASE_URL = "postgresql+asyncpg://postgres:passwd@localhost:5433/mortgagedb"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DB_URL= settings.DB_URL

engine = create_async_engine(
    DATABASE_URL
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
