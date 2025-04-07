from enums.event_enums import EventState
from models import Bet


async def create_bet_validator(response_dict: dict, bet: Bet) -> None:
    assert len(response_dict) == 7
    assert response_dict["id"] == str(bet.id)
    assert response_dict["name"] == bet.name
    assert response_dict["amount"] == int(bet.amount)
    assert EventState(response_dict["state"]) == bet.state
    assert response_dict["event_id"] == str(bet.event_id)
    assert "created_at" in response_dict
    assert response_dict["updated_at"] is None


async def get_bet_validator(response_dict: dict, bet: dict) -> None:
    assert len(response_dict) == 7
    assert response_dict["id"] == str(bet["id"])
    assert response_dict["name"] == bet["name"]
    assert response_dict["amount"] == int(bet["amount"])
    assert EventState(response_dict["state"]) == bet["state"]
    assert response_dict["event_id"] == bet["event_id"]
    assert "created_at" in response_dict
    assert "updated_at" in response_dict
