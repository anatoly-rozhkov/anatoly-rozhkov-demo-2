import time
import uuid
from datetime import datetime, timezone
from typing import Sequence, cast

from adapters.db.postgres import Database
from enums.event_enums import EventState
from fastapi import APIRouter, FastAPI, HTTPException
from interactors.bet_interactor import BetInteractor
from interactors.event_interactors import EventInteractor
from pydantic import ValidationError
from schemas.bet_schemas import (BetListSchema, BetResponseSchema,
                                 CreteBetSchema)
from starlette import status

app = FastAPI()
router = APIRouter(prefix="")


@router.post("/bets/", status_code=status.HTTP_201_CREATED)
async def create_bet(request: CreteBetSchema) -> BetResponseSchema:
    bet_id = uuid.uuid4()
    bet_interactor = BetInteractor()
    event_interactor = EventInteractor(Database.get_instance())

    data = request.model_dump()

    try:
        event = await event_interactor.get_event_by_id(uuid.UUID(data["event_id"]))
        if not event:
            raise HTTPException(status_code=404, detail="Event with this doesn't exist")

    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid event ID format")

    if event.deadline < time.time():
        raise HTTPException(status_code=400, detail="Event has already expired. Please, select another event")
    elif event.state != EventState.NEW:
        raise HTTPException(status_code=400, detail="Event has already completed. Please, select another event")

    await bet_interactor.create_bet(dict(id=bet_id, state=event.state, created_at=datetime.now(timezone.utc), **data))

    retrieved_bet = await bet_interactor.get_bet_by_id(bet_id)

    try:
        return BetResponseSchema(
            **{
                "id": retrieved_bet.id,
                "name": retrieved_bet.name,
                "created_at": retrieved_bet.created_at,
                "updated_at": retrieved_bet.updated_at,
                "amount": retrieved_bet.amount,
                "event_id": retrieved_bet.event_id,
                "state": retrieved_bet.state,
            }
        )
    except ValidationError:
        raise HTTPException(status_code=422, detail="Invalid data format")


@router.get("/bets/", status_code=status.HTTP_200_OK)
async def get_bets() -> BetListSchema:
    bets = await BetInteractor().get_bets()
    try:
        return BetListSchema(results=cast(Sequence[BetResponseSchema], bets))
    except ValidationError:
        raise HTTPException(status_code=422, detail="Invalid data format")
