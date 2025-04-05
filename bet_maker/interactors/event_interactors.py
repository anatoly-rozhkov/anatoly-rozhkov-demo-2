from adapters.db.postgres import Database
from models.event_models import Event


class EventInteractor:
    def __init__(self):
        self.db = Database.get_instance()

    # @staticmethod
    # async def get_valid_events() -> list:
    #     return [event for event in events if time.time() < event["deadline"]]

    async def create_event(self, event_data: dict) -> None:
        async with self.db.get_session() as session:
            session.add(Event(**event_data))
            await session.commit()
