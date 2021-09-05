
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

    def __str__(self) -> str:
        return f"Id: {self.entity_id}, type: {self.event_type}, new_state: {self.new_state}, old_state: {self.old_state}"
