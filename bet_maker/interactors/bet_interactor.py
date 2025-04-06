from datetime import datetime, timezone
from typing import Sequence, Union

from adapters.db.postgres import Database
from enums.event_enums import EventState
from models import Bet
from pydantic import UUID4
from sqlalchemy.future import select


class BetRepository:
    def __init__(self):
        self.db = Database.get_instance()

    async def get_bets(self) -> Sequence[Bet]:
        async with self.db.get_session() as session:
            result = await session.execute(select(Bet))
            return result.scalars().all()

    async def get_bet_by_id(self, bet_id: UUID4) -> Union[Bet, None]:
        async with self.db.get_session() as session:
            result = await session.execute(select(Bet).where(Bet.id == bet_id))
            return result.scalars().first()

    async def create_bet(self, data: dict) -> None:
        async with self.db.get_session() as session:
            session.add(Bet(**data))
            await session.commit()

    async def update_bet(self, event_id: UUID4, state: EventState) -> None:
        async with self.db.get_session() as session:
            bet = await session.execute(select(Bet).where(Bet.event_id == event_id))
            bet = bet.scalars().first()
            if bet:
                setattr(bet, "state", state)
                setattr(bet, "updated_at", datetime.now(timezone.utc))
                await session.commit()


class BetInteractor:
    def __init__(self, bet_repository: BetRepository = None):
        self.bet_repository = bet_repository or BetRepository()

    async def get_bets(self) -> Sequence[Bet]:
        return await self.bet_repository.get_bets()

    async def get_bet_by_id(self, bet_id: UUID4) -> Union[Bet, None]:
        return await self.bet_repository.get_bet_by_id(bet_id)

    async def create_bet(self, data: dict) -> None:
        await self.bet_repository.create_bet(data)

    async def update_bet(self, event_id: UUID4, state: EventState) -> None:
        await self.bet_repository.update_bet(event_id, state)
