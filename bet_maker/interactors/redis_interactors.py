import pickle

from adapters.redis.redis_client import redis_client
from core.settings import settings


async def store_in_redis(message) -> None:
    created_data = pickle.loads(message.body)
    await save_data(data=created_data)


async def save_data(data: dict) -> None:
    redis_keys_var = settings.redis.device_command_public_keys_var.format(redis_keys_var=data["id"])
    instance: bytes | dict = await redis_client.get(redis_keys_var) or {}

    if instance:
        instance = pickle.loads(instance)
    else:
        instance["id"] = data["id"]

    await redis_client.set(redis_keys_var, pickle.dumps(instance))
