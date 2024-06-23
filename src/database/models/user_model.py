from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

from src.database.models import Base
from src.database.models import MortgageOrm


class User(SQLAlchemyBaseUserTableUUID, Base):
    __table_args__ = {'extend_existing': True}
    payment_calculations: Mapped["MortgageOrm"] = relationship()
