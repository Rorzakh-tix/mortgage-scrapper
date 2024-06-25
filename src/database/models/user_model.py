from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

from database.models.base_model import Base
from database.models.mortgage_model import MortgageOrm


class User(SQLAlchemyBaseUserTableUUID, Base):
    __table_args__ = {'extend_existing': True}
    payment_calculations: Mapped["MortgageOrm"] = relationship()
