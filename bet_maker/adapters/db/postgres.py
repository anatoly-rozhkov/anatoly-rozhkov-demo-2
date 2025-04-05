import sqlalchemy
from adapters.db.connection_management import DBConnectionManagement
from core.settings import settings
from models import *
from models.base_models import metadata
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)


class Database(metaclass=DBConnectionManagement):
    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(
            settings.postgres.get_dsn(), pool_size=settings.postgres.pool_size, echo=False
        )
        self.session_class = sqlalchemy.orm.sessionmaker(bind=self.engine, class_=AsyncSession)

    async def set_tables(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    def get_session(self) -> AsyncSession:
        return self.session_class()

    async def close(self):
        await self.engine.dispose()

    @classmethod
    def get_instance(cls, instance_name: str = settings.postgres.db) -> "Database":
        return cls(instance_name)
