import asyncio
from contextlib import asynccontextmanager

from adapters.rabbitmq.consumer_pika_client import PikaConsumerClient
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer = PikaConsumerClient()
    loop = asyncio.get_event_loop()
    task = asyncio.create_task(consumer.consume(loop))
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
