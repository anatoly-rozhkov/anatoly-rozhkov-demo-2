import uuid

from fastapi import APIRouter, FastAPI
from schemas.bet_schemas import (BetListSchema, BetResponseSchema,
                                 CreteBetSchema)
from starlette import status

app = FastAPI()
router = APIRouter(prefix="")


@router.post("/bets/", status_code=status.HTTP_201_CREATED)
async def create_bet(request: CreteBetSchema) -> BetResponseSchema:
    bet_id = uuid.uuid4()
    data = request.model_dump()

    return BetResponseSchema(id=bet_id, **data)


@router.get("/bets/", status_code=status.HTTP_200_OK)
async def get_events() -> BetListSchema:
    pass
