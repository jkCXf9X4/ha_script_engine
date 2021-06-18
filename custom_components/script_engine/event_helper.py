
import logging

from homeassistant.const import (
    ATTR_NOW,
    EVENT_CORE_CONFIG_UPDATE,
    EVENT_STATE_CHANGED,
    EVENT_TIME_CHANGED,
    MATCH_ALL,
    SUN_EVENT_SUNRISE,
    SUN_EVENT_SUNSET,
)
from homeassistant.core import (
    CALLBACK_TYPE,
    Event,
    HomeAssistant,
    State,
    callback,
    split_entity_id,
)

class State:
    constructor = 1
    operate = 2
    destructor = 3



class Event_helper:

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._LOGGER = logging.getLogger(__name__)


    def register_event_tracker(self, id):
    
        @callback
        def state_change_listener(event: Event) -> None:
            """Handle specific state changes."""
            hass.async_run_job(
                action,
                event.data.get("entity_id"),
                event.data.get("old_state"),
                event.data.get("new_state"),
            )
        return hass.bus.async_listen(EVENT_STATE_CHANGED, state_change_listener)