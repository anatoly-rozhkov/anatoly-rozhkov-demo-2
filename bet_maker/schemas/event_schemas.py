import decimal
import enum
from typing import Dict, Union

from pydantic import UUID4, BaseModel, Field
from schemas.base_schemas import BaseSchema


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class BaseEventSchema(BaseSchema):
    coefficient: decimal.Decimal = Field(..., description="Coefficient")
    deadline: int = Field(..., description="Deadline in seconds")
    state: EventState = Field(..., description="Event state")


class EventListSchema(BaseModel):
    events: Dict[Union[UUID4, str], BaseEventSchema]
