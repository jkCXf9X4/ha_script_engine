
import logging

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

from custom_components.script_engine.event.event_wrapper import StateChangedEvent
from custom_components.script_engine.extension.singelton import Singleton


class EventDistributor(metaclass=Singleton):
    """
    Subscribes to home assistant event and distributes them to subscribers
    """
    
    def __init__(self, hass: HomeAssistant, debug=False) -> None:
        self.hass = hass
        self.log = logging.getLogger(__name__)
        self.id_table = {}
        self.debug = debug

        self._register_event_tracker()

    def _register_event_tracker(self):

        def pre_call(callback, event_data: StateChangedEvent):  # used to add event as a kwarg and not an arg
            not self.debug or self.log.debug(f"Executing callback {event_data.entity_id}, callback{ callback}")
            callback(event=event_data)

        @callback
        def state_change_listener(event: Event) -> None:
            event_data = StateChangedEvent(event)
            event_id = event_data.entity_id
            _ = [self.hass.async_run_job(pre_call, callback, event_data) for callback in self.id_table.get(event_id, [])]

        return self.hass.bus.async_listen(EVENT_STATE_CHANGED, state_change_listener)

    def register_callback(self, entity_id, callback):
        if entity_id not in self.id_table:
            self.id_table[entity_id] = []

        if callback not in self.id_table[entity_id]:
            self.id_table[entity_id].append(callback)
            not self.debug or self.log.debug(f"Added callback, {entity_id}: {callback}")
            return True
        return False

    def remove_callback(self, entity_id, callback):
        if entity_id in self.id_table and callback in self.id_table[entity_id]:
            self.id_table[entity_id].remove(callback)
            not self.debug or self.log.debug(f"Removed callback, {entity_id}: {callback}")
            return True
        return False

    def reset(self):
        self.id_table = {}

