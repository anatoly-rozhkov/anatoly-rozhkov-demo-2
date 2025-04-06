import time
import uuid
from datetime import datetime
from decimal import ROUND_UP, Decimal
from typing import Dict

from enums.event_enums import EventState
from tests.utils.factory_helpers import generate_random_string


def event_factory(
    name: str = generate_random_string(),
    state: EventState = EventState.NEW,
    coefficient: Decimal = Decimal(1.50),
    deadline_offset: float = 100.00,
) -> Dict:
    """
    Factory function to generate event data.

    :param name: The name of the event.
    :param state: The state of the event (use EventState).
    :param coefficient: The coefficient of the event.
    :param deadline_offset: Time offset for the event's deadline (default is 100).
    :return: A dictionary with event data.
    """
    return {
        "id": uuid.uuid4(),
        "name": name,
        "state": state,
        "updated_at": datetime.now(),
        "created_at": datetime.now(),
        "coefficient": coefficient.quantize(Decimal("0.01"), rounding=ROUND_UP),
        "deadline": Decimal(time.time() + deadline_offset).quantize(Decimal("0.01"), rounding=ROUND_UP),
    }
