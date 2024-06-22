from fastapi import APIRouter, Depends

from database.crud.mortgage_crud import create_mortgage_calculation
from database.models import User
from database.schemas.mortgage_schemas import MortgageCreate
from s3.minio import upload_file_to_s3
from scrapper.mortgage import MortgageInputData, get_website_mortgage_result_table
from users.users import current_active_user

mortgage_router = APIRouter(
)


@mortgage_router.post("/")
async def scrap(mortgage_data: MortgageInputData, user: User = Depends(
    current_active_user
)):
    result = await get_website_mortgage_result_table(mortgage_data)
    # add data to db
    mortgage_in = MortgageCreate(payments=result, user_id=user.id)
    return await create_mortgage_calculation(mortgage_in=mortgage_in)


@mortgage_router.get("/upload")
async def upload_to_s3(user: User = Depends(
    current_active_user
)):
    await upload_file_to_s3('page.pdf', str(user.id), 'payments_results.pdf')
