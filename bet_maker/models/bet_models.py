from enums.event_enums import EventState
from models.base_models import BaseModel, UpdatedAtModel
from sqlalchemy import DECIMAL, Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Bet(BaseModel, UpdatedAtModel):
    __tablename__ = "bets"

    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    event = relationship("Event", lazy="selectin")
    amount = Column(DECIMAL(precision=10, scale=2))
    state = Column(Enum(EventState, name="bet_state"))
