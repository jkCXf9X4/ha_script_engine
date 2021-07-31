
from datetime import datetime
import uuid

import logging

# https://github.com/home-assistant/core/blob/master/homeassistant/core.py
from homeassistant.core import (
    Event,
    State,
)

class StateChangedEvent:
    def __init__(self, event: Event) -> None:
        self.event: Event = event
        self.event_type = event.event_type
        self.entity_id = event.data.get("entity_id")
        self.new_state: State = event.data.get("new_state")
        self.old_state: State = event.data.get("old_state")

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, StateChangedEvent):
            return NotImplemented
        return self.event == self.event
