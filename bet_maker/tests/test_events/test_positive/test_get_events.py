import pytest
from models import Event
from tests.factories.event_factories import event_dict_factory
from tests.response_validation_helpers.event_validators import \
    get_event_validator
from tests.utils.iterable_object_validators import validate_iterable_objects


@pytest.mark.asyncio
async def test_get_events(async_client, local_session):
    # When
    data = [event_dict_factory() for _ in range(2)]
    for item in data:
        event = Event(**item)
        local_session.add(event)
    await local_session.commit()

    # Then
    response = await async_client.get("/api/events/")

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 200

    assert len(response_data["results"]) == 2
    await validate_iterable_objects(response_data["results"], data, get_event_validator)


@pytest.mark.asyncio
async def test_get_events_when_they_are_outdated(async_client, local_session):
    # When
    data = [event_dict_factory(deadline_offset=-100) for _ in range(2)]
    for item in data:
        event = Event(**item)
        local_session.add(event)
    await local_session.commit()

    # Then
    response = await async_client.get("/api/events/")

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 200

    assert len(response_data["results"]) == 0
    assert len(data) == 2
