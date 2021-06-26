import logging

class Engine:

    def __init__(self, *args, **kwargs) -> None:
        self.hass = kwargs.get('hass', None)
        self.log: logging.Logger = kwargs.get('logger', logging.getLogger(__name__))
        self.domain = kwargs.get('domain', "unknown_domain")

        # self.log.info("Engine init")

    def set_state(self, state_name, new_state):
        self.log.info("set state")
        self.hass.states.async_set(f"{self.domain}.{state_name}", new_state)

    def get_state(self, entity_id):
        return self.hass.states.get(entity_id)


