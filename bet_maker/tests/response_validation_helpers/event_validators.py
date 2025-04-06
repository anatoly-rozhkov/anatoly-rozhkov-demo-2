from enums.event_enums import EventState


async def get_event_validator(response_dict: dict, event: dict) -> None:
    assert len(response_dict) == 7
    assert response_dict["id"] == str(event["id"])
    assert response_dict["name"] == event["name"]
    assert response_dict["coefficient"] == str(event["coefficient"])
    assert EventState(response_dict["state"]) == event["state"]
    assert response_dict["deadline"] == str(event["deadline"])
    assert "created_at" in response_dict
    assert "updated_at" in response_dict
