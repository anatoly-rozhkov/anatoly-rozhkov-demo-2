from fastapi import APIRouter
from routers.bet_maker.bet_router import router as bet_router
from routers.bet_maker.event_router import router as event_router

main_router = APIRouter(prefix="/api")
main_router.include_router(event_router, tags=["Events"])
main_router.include_router(bet_router, tags=["Bets"])
