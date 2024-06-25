import os
from functools import lru_cache
from typing import Optional

from pydantic import field_validator, SecretStr
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

AWS_SECRET = os.environ.get("AWS_SECRET")
AWS_ACCESS = os.environ.get("AWS_ACCESS")

class DBSettings(BaseSettings):
    PGHOST: str
    PGUSER: str
    PGPASSWORD: SecretStr
    PGDATABASE: str
    DATABASE_URI: str = ''

    @field_validator('DATABASE_URI', mode='before')
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> str:
        user = info.data.get('PGUSER', '')
        password = info.data.get('PGPASSWORD', '')
        server = info.data.get('PGHOST', '')
        db = info.data.get('PGDATABASE')
        return f'postgresql+asyncpg://{user}:{password.get_secret_value()}@{server}/{db}'

    model_config = SettingsConfigDict(
        env_file='.env',
        frozen=True,
        extra='ignore',
    )


@lru_cache
def create_db_settings() -> DBSettings:
    return DBSettings()