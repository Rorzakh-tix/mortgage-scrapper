from fastapi import APIRouter, Depends

from database.models.user_model import User
from src.database.crud.mortgage_crud import add_mortgage_calculation
from src.database.schemas.mortgage_schemas import MortgageCreate
from src.s3.minio import upload_file_to_s3
from src.scrapper.mortgage import MortgageInputData, get_website_mortgage_result_table
from src.users.users import current_active_user

mortgage_router = APIRouter(
)


@mortgage_router.post("/")
async def scrap(mortgage_data: MortgageInputData, user: User = Depends(
    current_active_user
)):
    result = await get_website_mortgage_result_table(mortgage_data)
    # add data to db
    mortgage_in = MortgageCreate(payments=result, user_id=user.id)
    return await add_mortgage_calculation(mortgage_in=mortgage_in)


@mortgage_router.get("/upload")
async def upload_to_s3(user: User = Depends(
    current_active_user
)):
    await upload_file_to_s3('page.pdf', "pdf-payments", f"{str(user.id)}payments_results.pdf")
