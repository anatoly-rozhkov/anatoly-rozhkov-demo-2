import time

from fastapi import APIRouter, FastAPI
from interactors.redis_interactors import get_events_for_redis
from schemas.event_schemas import EventListSchema
from starlette import status

app = FastAPI()
router = APIRouter(prefix="/events")


@router.get("/events/", status_code=status.HTTP_200_OK)
async def get_events() -> EventListSchema:
    events = await get_events_for_redis()
    return EventListSchema(events=[event for event in events if time.time() < event["deadline"]])
