import logging

from custom_components.script_engine.const import DOMAIN

class Engine:

    def __init__(self, *args, **kwargs) -> None:
        self.hass = kwargs.get('hass', None)
        self.log = kwargs.get('logger', logging.getLogger(__name__))
        self.domain = kwargs.get('domain', "unknown_domain")

    @staticmethod
    def get_local_id(id):
        return f"{DOMAIN}.{id}"

    def set_state(self, entity_id, new_state):
        self.log.info(f"set state, {entity_id}, {new_state}")
        self.hass.states.async_set(entity_id, new_state)

    def set_local_state(self, entity_id, new_state):
        self.log.info(f"set state, {entity_id}, {new_state}")
        self.hass.states.async_set(Engine.get_local_id(entity_id), new_state)

    def get_state(self, entity_id):
        value = self.hass.states.get(entity_id)
        self.log.info(f"get state, {entity_id}, {value}")
        return value

    def get_local_state(self, entity_id):
        value = self.hass.states.get(Engine.get_local_id(entity_id))
        self.log.info(f"get state, {entity_id}, {value}")
        return value

    def call_service(self, service, action, id, data={}):
        data["entity_id"] = id
        self.hass.services.call(service, action, service, data)

    def turn_on_light(self, id, data={}):
        self.call_service("light", "turn_on", id, data)

    def turn_off_light(self, id, data={}):
        self.call_service("light", "turn_off", id, data)


