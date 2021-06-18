import logging

class Engine:

    @staticmethod
    def event_decorator(func):
        def event_setter_function(*args, **kwargs):
            #register event handlr
            args[0].log.info("in decorator")

            return_value = func(*args, **kwargs)
            return return_value
        return event_setter_function

    def __init__(self, *args, **kwargs) -> None:
        self.hass = kwargs.get('hass', None)
        self.log = logging.getLogger(kwargs.get('log_name', type(self).__name__))
        self.domain = kwargs.get('domain', "no_domain")

        self.log.info("Engine init")

    def set_state(self, state_name, new_state):
        self.log.info("set state")
        self.hass.states.async_set(f"{self.domain }.{state_name}", new_state)

