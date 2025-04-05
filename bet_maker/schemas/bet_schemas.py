from typing import List, Union

from pydantic import UUID4, BaseModel, Field
from schemas.base_schemas import BaseResponseSchema, BaseSchema


class CreteBetSchema(BaseSchema):
    amount: int = Field(..., description="Bet amount", ge=1)
    event: Union[UUID4, str] = Field(..., description="Event ID")


class BetResponseSchema(BaseResponseSchema, CreteBetSchema):
    pass


class BetListSchema(BaseModel):
    bets: List[BetResponseSchema]
