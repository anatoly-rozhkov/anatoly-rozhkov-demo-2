from typing import Sequence, cast

from adapters.db.postgres import Database
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from interactors.event_interactors import EventInteractor
from pydantic import ValidationError
from schemas.event_schemas import EventListSchema, EventResponseSchema
from starlette import status

app = FastAPI()
router = APIRouter(prefix="")


@router.get("/events/", status_code=status.HTTP_200_OK)
async def get_events(database: Database = Depends(Database.get_instance)) -> EventListSchema:
    valid_events = await EventInteractor(db=database).get_valid_events()
    try:
        return EventListSchema(results=cast(Sequence[EventResponseSchema], valid_events))
    except ValidationError:
        raise HTTPException(status_code=422, detail="Invalid data format")
