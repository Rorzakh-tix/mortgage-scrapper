from src.database.base import async_session_maker
from src.database.models import MortgageOrm
from src.database.schemas.mortgage_schemas import MortgageCreate


async def create_mortgage_calculation(
        mortgage_in: MortgageCreate
) -> MortgageOrm:
    async with async_session_maker() as session:
        mortgage_calculation = MortgageOrm(**mortgage_in.model_dump())
        session.add(mortgage_calculation)
        await session.commit()
        return mortgage_calculation
