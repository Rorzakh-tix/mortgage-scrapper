from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

from database.models import Base
from database.models import MortgageOrm


class User(SQLAlchemyBaseUserTableUUID, Base):
    payment_calculations: Mapped["MortgageOrm"] = relationship()
