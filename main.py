import asyncio
from contextlib import asynccontextmanager

from playwright.async_api import Playwright, async_playwright

from database.base import User, create_db_and_tables
from scrapper.hypotec import get_website_content, get_website_content2
from users.schemas import UserCreate, UserRead, UserUpdate
from users.users import auth_backend, current_active_user, fastapi_users_ep
from fastapi import FastAPI, Depends
import uvicorn




@asynccontextmanager
async def lifespan(app: FastAPI):
    # before starting
    # db connection etc
    await create_db_and_tables()
    yield
    #


app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users_ep.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users_ep.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users_ep.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users_ep.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users_ep.get_users_router(UserRead, UserUpdate), prefix="/auth", tags=["auth"])


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    await get_website_content()
    return {"message": f"Hello {user.email}!"}


@app.get("/scrap", tags=["scrapping"])
async def scrap():
    await get_website_content2()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=False, log_level="info")