import pytest
from models import Bet, Event
from tests.factories.bet_factories import bet_dict_factory
from tests.factories.event_factories import event_dict_factory
from tests.response_validation_helpers.bet_validators import get_bet_validator
from tests.utils.iterable_object_validators import validate_iterable_objects


@pytest.mark.asyncio
async def test_get_bets(async_client, local_session):
    # When
    # Create event first
    event_data = event_dict_factory()
    local_session.add(Event(**event_data))
    await local_session.commit()

    data = [bet_dict_factory(event_id=event_data["id"]) for _ in range(2)]
    for item in data:
        event = Bet(**item)
        local_session.add(event)
    await local_session.commit()

    # Then
    response = await async_client.get("/api/bets/")

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 200

    assert len(response_data["results"]) == 2
    await validate_iterable_objects(response_data["results"], data, get_bet_validator)
