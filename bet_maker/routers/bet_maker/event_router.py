from typing import Sequence, cast

from fastapi import APIRouter, FastAPI, HTTPException
from interactors.event_interactors import EventInteractor
from pydantic import ValidationError
from schemas.event_schemas import EventListSchema, EventResponseSchema
from starlette import status

app = FastAPI()
router = APIRouter(prefix="")


@router.get("/events/", status_code=status.HTTP_200_OK)
async def get_events() -> EventListSchema:
    valid_events = await EventInteractor().get_valid_events()
    try:
        return EventListSchema(results=cast(Sequence[EventResponseSchema], valid_events))
    except ValidationError:
        raise HTTPException(status_code=422, detail="Invalid data format")
