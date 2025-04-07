import pytest
from enums.event_enums import EventState
from models import Event
from tests.factories.bet_factories import create_bet_dict_factory
from tests.factories.event_factories import event_dict_factory


@pytest.mark.asyncio
async def test_create_bet_field_validation(async_client, local_session):
    # Then
    response = await async_client.post("/api/bets/", json={})

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 422

    # Validate error messages
    errors = response_data["errors"]
    assert errors[0]["detail"] == "Field required"
    assert errors[1]["detail"] == "Field required"
    assert errors[2]["detail"] == "Field required"

    assert errors[0]["message"][1] == "name"
    assert errors[1]["message"][1] == "amount"
    assert errors[2]["message"][1] == "event_id"


@pytest.mark.asyncio
async def test_create_bet_invalid_event_id(async_client, local_session):
    # Then
    response = await async_client.post("/api/bets/", json=create_bet_dict_factory(event_id="invalid_id"))

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 400

    # Validate error messages
    assert response_data["detail"] == "Invalid event ID format"


@pytest.mark.asyncio
async def test_create_bet_event_doesnt_exist(async_client, local_session):
    # Then
    response = await async_client.post("/api/bets/", json=create_bet_dict_factory())

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 404

    # Validate error messages
    assert response_data["detail"] == "Event with this doesn't exist"


@pytest.mark.asyncio
async def test_create_bet_expired_event(async_client, local_session):
    # Create event first
    event_data = event_dict_factory(deadline_offset=-100)
    local_session.add(Event(**event_data))
    await local_session.commit()

    # Then
    response = await async_client.post("/api/bets/", json=create_bet_dict_factory(event_id=event_data["id"]))

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 400

    # Validate error messages
    assert response_data["detail"] == "Event has already expired. Please, select another event"


@pytest.mark.asyncio
async def test_create_bet_finished_event(async_client, local_session):
    # Create event first
    event_data = event_dict_factory(state=EventState.FINISHED_WIN)
    local_session.add(Event(**event_data))
    await local_session.commit()

    # Then
    response = await async_client.post("/api/bets/", json=create_bet_dict_factory(event_id=event_data["id"]))

    try:
        response_data = response.json()
    except TypeError:
        response_data = response

    assert response.status_code == 400

    # Validate error messages
    assert response_data["detail"] == "Event has already completed. Please, select another event"
