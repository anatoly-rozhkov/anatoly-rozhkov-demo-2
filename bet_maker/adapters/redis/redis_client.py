import redis.asyncio as redis
from core.settings import settings

redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password.get_secret_value(),
    db=settings.redis.db_session,
)
