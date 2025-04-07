import uuid

import pytest_asyncio
from adapters.db.postgres import Database
from core.settings import settings
from httpx import ASGITransport, AsyncClient
from main import app
from models import *
from models.base_models import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


@pytest_asyncio.fixture
async def create_new_database(name: str = f"test_{uuid.uuid4().hex}"):
    """Fixture that creates a new database for each test and drops it after the test."""
    default_engine = create_async_engine(settings.postgres.get_external_dsn("postgres"), echo=True)

    # Create new DB
    async with default_engine.connect() as connection:
        # Avoid transactions when creating a database
        connection = await connection.execution_options(isolation_level="AUTOCOMMIT")
        await connection.execute(text(f"CREATE DATABASE {name}"))

    # Run migrations
    new_database = Database.get_instance(name, True)
    async with new_database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    try:
        yield new_database
    finally:
        # Clean up: Drop the database after the test
        await new_database.engine.dispose()
        async with default_engine.connect() as connection:
            connection = await connection.execution_options(isolation_level="AUTOCOMMIT")
            await connection.execute(text(f"DROP DATABASE IF EXISTS {name}"))


@pytest_asyncio.fixture
async def local_session(create_new_database):
    """Fixture that creates a session for the newly created test database."""
    async with create_new_database.get_session() as session:
        yield session


@pytest_asyncio.fixture
async def async_client(create_new_database):
    """Fixture to initialize an AsyncClient for each test."""

    async def override_get_db():
        yield create_new_database

    app.dependency_overrides[Database.get_instance] = override_get_db

    # I've probably spent 3 hours trying to figure out how to make mock dbs similar to django_db with that mf chatgpt.
    # My figuring out how to do this despite all the misleading hints from gpt
    # is the greatest victory of humanity over machines to date
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
