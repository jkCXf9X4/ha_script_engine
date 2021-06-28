import logging

class Engine:

    def __init__(self, *args, **kwargs) -> None:
        self.hass = kwargs.get('hass', None)
        self.log = logging.getLogger(__name__)  # kwargs.get('logger', logging.getLogger(__name__))
        self.domain = kwargs.get('domain', "unknown_domain")

        # self.log.info("Engine init")

    def set_state(self, entity_id, new_state):
        self.log.info(f"set state, {entity_id}, {new_state}")
        self.hass.states.async_set(f"{self.domain}.{entity_id}", new_state)

    def get_state(self, entity_id):
        value = self.hass.states.get(entity_id)
        self.log.info(f"get state, {entity_id}, {value}")
        return value


