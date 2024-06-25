from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.base import create_db_and_tables
from src.database.schemas.user_schemas import UserCreate, UserRead, UserUpdate
from src.scrapper.endpoints import mortgage_router
from src.users.users import auth_backend, fastapi_users_ep


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before starting
    await create_db_and_tables()
    yield
    #


app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users_ep.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users_ep.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users_ep.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users_ep.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users_ep.get_users_router(UserRead, UserUpdate), prefix="/auth", tags=["auth"])
app.include_router(router=mortgage_router,prefix="/scrap", tags=["scraping"])


if __name__ == '__main__':
    uvicorn.run("main:app", reload=False, log_level="info")
