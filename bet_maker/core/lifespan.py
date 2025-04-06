import asyncio
from contextlib import asynccontextmanager

from adapters.db.postgres import Database
from adapters.rabbitmq.consumer_pika_client import PikaConsumerClient
from core.settings import settings
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer = PikaConsumerClient()
    loop = asyncio.get_event_loop()
    task = asyncio.create_task(consumer.consume(loop))
    await Database(settings.postgres.db).set_tables()
    try:
        yield
    finally:
        task.cancel()
        await Database(settings.postgres.db).close()
        try:
            await task
        except asyncio.CancelledError:
            pass
