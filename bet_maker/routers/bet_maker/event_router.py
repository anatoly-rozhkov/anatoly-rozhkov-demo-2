from fastapi import APIRouter, FastAPI
from schemas.event_schemas import EventListSchema
from starlette import status

app = FastAPI()
router = APIRouter(prefix="/events")


@router.get("/events/", status_code=status.HTTP_200_OK)
async def get_events() -> EventListSchema:
    pass
    # return EventListSchema(
    #     events={event_id: event for event_id, event in data_storage.data.items() if time.time() < event.deadline}
    # )
