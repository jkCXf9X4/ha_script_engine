import homeassistant
import logging

from homeassistant.core import State, HomeAssistant

class StateExt:

    _logger = logging.getLogger(__name__)

    @classmethod
    def set_state(cls, hass: HomeAssistant, entity_id: str, new_state: str, attributes=None, force_update=False, debug=False) -> None:
        hass.states.async_set(entity_id, new_state=new_state, attributes=attributes, force_update=force_update)
        not debug or cls._logger.debug(f"set state, {entity_id},State: {new_state}, Att: {attributes}, Force: {force_update}")

    @classmethod
    def get_state(cls, hass: HomeAssistant, entity_id, debug=False) -> State:
        value = hass.states.get(entity_id)
        not debug or cls._logger.debug(f"get state, {entity_id}, {value}")
        return value

    @classmethod
    def get_ids_from_group(cls, hass: HomeAssistant, group_id, debug=False):
        group_state = hass.states.get(group_id)
        group = group_state.attributes["entity_id"]
        not debug or cls._logger.debug(group_state.as_dict())
        return group
