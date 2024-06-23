import uuid

from sqlalchemy import ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import Base


class MortgageOrm(Base):
    __tablename__ = "payment_calculation"
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    payments: Mapped[ARRAY] = mapped_column(type_=JSONB, nullable=False)
