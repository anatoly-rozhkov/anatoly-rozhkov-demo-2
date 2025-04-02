from fastapi import APIRouter
from routers.bet_maker.event_router import router as event_router

main_router = APIRouter(prefix="/api")
main_router.include_router(event_router, tags=["Events"])
