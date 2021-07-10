
import logging

from .misc import Singleton

from homeassistant.const import (
    # ATTR_NOW,
    # EVENT_CORE_CONFIG_UPDATE,
    EVENT_STATE_CHANGED,
    # EVENT_TIME_CHANGED,
    # MATCH_ALL,
    # SUN_EVENT_SUNRISE,
    # SUN_EVENT_SUNSET,
)
from homeassistant.core import (
    # CALLBACK_TYPE,
    Event,
    HomeAssistant,
    # State,
    callback,
    # split_entity_id,
)

from custom_components.script_engine.local_event_wrapper import LocalEventWrapper

class EventDistributor(metaclass=Singleton):

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.log = logging.getLogger(__name__)
        self.id_table = {}

        self._register_event_tracker()

    def _register_event_tracker(self):

        def pre_call(callback, event_data):  # used to add event as a kwarg and not an arg
            # self.log.debug(f"executing callback {id}, callback{ callback}")
            callback(self, event=event_data)

        @callback
        def state_change_listener(event: Event) -> None:
            event_data = LocalEventWrapper(event)
            id = event_data.id
            if id in self.id_table:
                _ = [self.hass.async_run_job(pre_call, callback, event_data) for callback in self.id_table[id]]

        return self.hass.bus.async_listen(EVENT_STATE_CHANGED, state_change_listener)

    def register_callback(self, id, callback):
        if id not in self.id_table:
            self.id_table[id] = []

        if callback not in self.id_table[id]:
            # self.log.debug(f"Adding callback {id}")
            self.id_table[id].append(callback)

    def reset(self):
        self.id_table = {}

