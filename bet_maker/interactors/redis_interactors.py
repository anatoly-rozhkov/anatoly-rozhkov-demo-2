import pickle

from adapters.redis.redis_client import redis_client


async def store_in_redis(message: dict) -> None:
    await save_event(message)


async def save_event(data: dict) -> None:
    events: bytes = await redis_client.get("events")
    events: list = pickle.loads(events) if events else []

    events.append(data)

    await redis_client.set("events", pickle.dumps(events))


async def get_events_for_redis() -> list:
    events: bytes = await redis_client.get("events")
    return pickle.loads(events) if events else []
