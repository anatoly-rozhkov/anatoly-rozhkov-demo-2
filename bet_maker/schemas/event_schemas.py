import decimal
from decimal import Decimal
from typing import List

from enums.event_enums import EventState
from pydantic import BaseModel, Field
from schemas.base_schemas import BaseResponseSchema, BaseSchema


class BaseEventSchema(BaseSchema):
    coefficient: decimal.Decimal = Field(..., description="Coefficient", ge=Decimal("1.01"))
    deadline: decimal.Decimal = Field(..., description="Deadline in seconds", ge=Decimal("30.00"))
    state: EventState = Field(..., description="Event state")


class EventResponseSchema(BaseResponseSchema, BaseEventSchema):
    pass


class EventListSchema(BaseModel):
    events: List[EventResponseSchema]
