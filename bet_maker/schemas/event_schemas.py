import decimal
import enum
from decimal import Decimal
from typing import List, Union

from pydantic import UUID4, BaseModel, Field
from schemas.base_schemas import BaseSchema


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class BaseEventSchema(BaseSchema):
    coefficient: decimal.Decimal = Field(..., description="Coefficient", ge=Decimal("1.01"))
    deadline: decimal.Decimal = Field(..., description="Deadline in seconds", ge=Decimal("30.00"))
    state: EventState = Field(..., description="Event state")


class ResponseEventSchema(BaseEventSchema):
    id: Union[UUID4, str] = Field(description="Event ID")


class EventListSchema(BaseModel):
    events: List[ResponseEventSchema]
