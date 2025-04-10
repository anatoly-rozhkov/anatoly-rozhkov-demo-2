import logging
import pickle

import aio_pika
import aio_pika.abc
from adapters.db.postgres import Database
from core.settings import settings
from interactors.event_interactors import EventInteractor

logger = logging.getLogger()


class PikaConsumerClient:
    def __init__(self, loop=None) -> None:
        self.consumer_queue_name = settings.rabbit.pika_consumer_queue_name

    async def consume(self, loop):
        """Setup message listener"""
        try:
            connection: aio_pika.abc.AbstractConnection = await aio_pika.connect_robust(
                host=settings.rabbit.host,
                port=settings.rabbit.port,
                login=settings.rabbit.login,
                password=settings.rabbit.password,
                loop=loop,
            )
        except ConnectionError as ex:
            exception_message = ex.args[0]
            logger.error("Failed to connect to broker %s", exception_message)

        async with connection:
            channel: aio_pika.abc.AbstractChannel = await connection.channel()

            # Declaring queue
            queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(self.consumer_queue_name, auto_delete=False)

            async with queue.iterator() as queue_iter:
                # Cancel consuming after __aexit__
                async for message in queue_iter:
                    async with message.process():
                        try:
                            received_message: dict = pickle.loads(message.body)
                            logger.warning("Received message %s", received_message)
                            await EventInteractor(Database.get_instance()).update_or_create_event(received_message)
                        except Exception as db_exception:
                            logger.error("Message failed to add to DB. Details: %s", db_exception, exc_info=True)
