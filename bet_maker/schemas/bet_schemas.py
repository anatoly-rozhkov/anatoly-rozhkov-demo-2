from typing import List, Sequence, Union

from enums.event_enums import EventState
from pydantic import UUID4, BaseModel, Field
from schemas.base_schemas import BaseResponseSchema, BaseSchema


class CreteBetSchema(BaseSchema):
    name: str = Field(..., description="Name")
    amount: int = Field(..., description="Bet amount", ge=1)
    event_id: Union[UUID4, str] = Field(..., description="Event ID")


class BetResponseSchema(BaseResponseSchema, CreteBetSchema):
    state: EventState = Field(..., description="Bet state")


class BetListSchema(BaseModel):
    results: Sequence[BetResponseSchema] = Field(..., description="List of bets")
