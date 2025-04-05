from fastapi import APIRouter, FastAPI
from interactors.event_interactors import EventInteractor
from schemas.event_schemas import EventListSchema
from starlette import status

app = FastAPI()
router = APIRouter(prefix="")


@router.get("/events/", status_code=status.HTTP_200_OK)
async def get_events() -> EventListSchema:
    valid_events = await EventInteractor().get_valid_events()
    return EventListSchema(events=valid_events)
