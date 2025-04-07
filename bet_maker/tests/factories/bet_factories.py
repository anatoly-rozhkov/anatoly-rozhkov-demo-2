import uuid
from datetime import datetime
from decimal import ROUND_UP, Decimal
from typing import Dict, Union

from enums.event_enums import EventState
from pydantic import UUID4
from tests.utils.factory_helpers import generate_random_string


def create_bet_dict_factory(
    name: str = generate_random_string(),
    state: EventState = EventState.NEW.value,
    event_id: Union[str, UUID4] = uuid.uuid4(),
    amount: float = 100.00,
) -> Dict:
    """
    Factory function to generate bet data.

    :param name: The name of the bet.
    :param state: The state of the bet (use EventState).
    :param event_id: The ID of the event associated with the bet.
    :param amount: The amount of the bet.
    :return: A dictionary with bet data.
    """
    return {"name": name, "state": state, "event_id": str(event_id), "amount": amount}


def bet_dict_factory(
    name: str = generate_random_string(),
    state: EventState = EventState.NEW,
    event_id: Union[str, UUID4] = uuid.uuid4(),
    amount: Decimal = Decimal(100.00),
) -> Dict:
    """
    Factory function to generate bet data.

    :param name: The name of the bet.
    :param state: The state of the bet (use EventState).
    :param event_id: The ID of the event associated with the bet.
    :param amount: The amount of the bet.
    :return: A dictionary with bet data.
    """
    return {
        "id": uuid.uuid4(),
        "name": name,
        "state": state,
        "event_id": str(event_id),
        "amount": amount.quantize(Decimal("0.01"), rounding=ROUND_UP),
        "updated_at": datetime.now(),
        "created_at": datetime.now(),
    }
