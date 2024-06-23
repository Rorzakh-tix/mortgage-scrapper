import uuid
from typing import List, Dict, Any

from pydantic import BaseModel, ConfigDict


class MortgageBase(BaseModel):
    user_id: uuid.UUID
    payments: List[Dict[str, Any]]


class MortgageCreate(MortgageBase):
    pass


class Mortgage(MortgageBase):
    model_config = ConfigDict(from_attributes=True)
