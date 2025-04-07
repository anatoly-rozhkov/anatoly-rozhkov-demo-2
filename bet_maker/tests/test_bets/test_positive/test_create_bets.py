import pytest
from models import Bet, Event
from sqlalchemy import func
from sqlalchemy.future import select
from tests.factories.bet_factories import create_bet_dict_factory
from tests.factories.event_factories import event_dict_factory
from tests.response_validation_helpers.bet_validators import \
    create_bet_validator


@pytest.mark.asyncio
async def test_create_bet(async_client, local_session):
    # When
    # Create event first
    event_data = event_dict_factory()
    local_session.add(Event(**event_data))
    await local_session.commit()

    bet_data = create_bet_dict_factory(event_id=event_data["id"])

    # Then
    response = await async_client.post("/api/bets/", json=bet_data)

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 201

    # Retrieve the bet from the database
    result = await local_session.execute(select(Bet))
    created_bet = result.scalars().first()

    # Count num of created objects
    bet_count = await local_session.execute(select(func.count()).select_from(Bet))
    assert bet_count.scalar_one() == 1

    await create_bet_validator(response_data, created_bet)
