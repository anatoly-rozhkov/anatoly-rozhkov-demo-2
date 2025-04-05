from enums.event_enums import EventState
from models.base_models import BaseModel, UpdatedAtModel
from sqlalchemy import DECIMAL, Column, Enum


class Event(BaseModel, UpdatedAtModel):
    __tablename__ = "events"

    coefficient = Column(DECIMAL(precision=10, scale=2), nullable=False)
    deadline = Column(DECIMAL(precision=30, scale=2), nullable=False)
    state = Column(Enum(EventState, name="event_state"))
