from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

from library.database.models.base_model import Base
from scrapper.mortgage_model import Mortgage


class User(SQLAlchemyBaseUserTableUUID, Base):
    __table_args__ = {'extend_existing': True}
    payment_calculations: Mapped["Mortgage"] = relationship()
