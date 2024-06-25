from fastapi import APIRouter, Depends

from library.database.database import async_session_maker
from library.s3.minio import upload_file_to_s3
from scrapper.mortgage_model import Mortgage
from users.user_model import User
from src.scrapper.mortgage_scrapper import MortgageInputData, get_website_mortgage_result_table
from src.users.user_manager import current_active_user

mortgage_router = APIRouter(
)


@mortgage_router.post("/")
async def scrap(mortgage_data: MortgageInputData, user: User = Depends(
    current_active_user
)):
    result = await get_website_mortgage_result_table(mortgage_data)
    async with async_session_maker() as session:
        mortgage_calculation = Mortgage(payments=result, user_id=user.id)
        session.add(mortgage_calculation)
        await session.commit()
        return mortgage_calculation


@mortgage_router.get("/upload")
async def upload_to_s3(user: User = Depends(
    current_active_user
)):
    await upload_file_to_s3('page.pdf', "pdf-payments", f"{str(user.id)}payments_results.pdf")
