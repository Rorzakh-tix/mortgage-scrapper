from pydantic_settings import BaseSettings

DATABASE_URL = "postgresql+asyncpg://postgres:passwd@localhost:5433/mortgagedb"


class Settings(BaseSettings):
    db_url: str
    db_echo: bool = False


settings = Settings(
    db_url=DATABASE_URL
)
