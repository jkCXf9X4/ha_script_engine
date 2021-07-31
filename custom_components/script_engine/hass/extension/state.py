import logging

from homeassistant.core import State

class StateExt:

    _logger = logging.getLogger(__name__)

    @classmethod
    def set_state(cls, hass, entity_id, new_state, debug=False):
        not debug or cls._logger.debug(f"set state, {entity_id}, {new_state}")
        hass.states.async_set(entity_id, new_state)

    @classmethod
    def get_state(cls, hass, entity_id, debug=False) -> State:
        value = hass.states.get(entity_id)
        not debug or cls._logger.debug(f"get state, {entity_id}, {value}")
        return value

    @classmethod
    def get_ids_from_group(cls, hass, id, debug=False):
        group_state = cls.get_state(hass, id, debug=debug)
        group = group_state.attributes["entity_id"]
        not debug or cls._logger.debug(group_state.as_dict())
        return group
