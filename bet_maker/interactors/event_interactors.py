import time
from typing import Sequence, Union

from adapters.db.postgres import Database
from interactors.bet_interactor import BetInteractor
from models.event_models import Event
from pydantic import UUID4
from sqlalchemy.future import select


class EventRepository:
    def __init__(self):
        self.db = Database.get_instance()

    async def get_valid_events(self) -> Sequence[Event]:
        async with self.db.get_session() as session:
            result = await session.execute(select(Event).where(Event.deadline > time.time()))
            return result.scalars().all()

    async def get_event_by_id(self, event_id: UUID4) -> Union[Event, None]:
        async with self.db.get_session() as session:
            result = await session.execute(select(Event).where(Event.id == event_id))
            return result.scalars().first()

    async def update_event(self, update_data: dict) -> bool:
        state = False
        async with self.db.get_session() as session:
            event = await session.execute(select(Event).where(Event.id == update_data["id"]))
            event = event.scalars().first()
            if event:
                for key, value in update_data.items():
                    setattr(event, key, value)
                await session.commit()
                state = True

        if state:
            await BetInteractor().update_bet(update_data["id"], update_data["state"])
        return state

    async def create_event(self, event_data: dict) -> None:
        async with self.db.get_session() as session:
            session.add(Event(**event_data))
            await session.commit()


class EventInteractor:
    def __init__(self, event_repository: EventRepository = None):
        self.event_repository = event_repository or EventRepository()

    async def get_valid_events(self) -> Sequence[Event]:
        return await self.event_repository.get_valid_events()

    async def get_event_by_id(self, event_id: UUID4) -> Union[Event, None]:
        return await self.event_repository.get_event_by_id(event_id)

    async def update_or_create_event(self, event_data: dict):
        update_event = await self.event_repository.update_event(event_data)
        if not update_event:
            await self.event_repository.create_event(event_data)
