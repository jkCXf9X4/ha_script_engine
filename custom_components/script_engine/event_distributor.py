
import logging

from .misc import Singleton

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

class EventData:
    def __init__(self, event) -> None:
        self.id, self.new_state, self.old_state = self.extract_event_states(event)

    def extract_event_states(self, event):
        id = event.data.get("entity_id")
        new_state = event.data.get("new_state").state
        old_state = event.data.get("old_state")

        if old_state != None:
            old_state = old_state.state

        return id, new_state, old_state


class EventDistributor(metaclass=Singleton):

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.log = logging.getLogger(__name__)
        self.id_table = {}

        self._register_event_tracker()

    def _register_event_tracker(self):

        @callback
        def state_change_listener(event: Event) -> None:
            event_data = EventData(event)
            id = event_data.id
            if id in self.id_table:
                self._exec_callback(id, event_data)

        return self.hass.bus.async_listen(EVENT_STATE_CHANGED, state_change_listener)

    def _exec_callback(self, id, event_data):
        def pre_call(callback, event_data):
            # self.log.debug(f"executing callback {id}, callback{ callback}")
            callback(self, event=event_data)

        for call in self.id_table[id]:
            self.hass.async_run_job(pre_call, call, event_data)

    def register_callback(self, id, callback):
        if id not in self.id_table:
            self.id_table[id] = []

        if callback not in self.id_table[id]:
            # self.log.debug(f"Adding callback {id}")
            self.id_table[id].append(callback)

    def reset(self):
        self.id_table = {}

