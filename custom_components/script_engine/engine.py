import logging

class Engine:

    @staticmethod
    def event_decorator(func):
        def event_setter_function(*args, **kwargs):
            #register event handlr
            print("in decorator")
            return_value = func(*args, **kwargs)
            return return_value
        return event_setter_function

    def __init__(self, *args, **kwargs) -> None:
        self.hass = kwargs.get('hass', None)
        self.log = logging.getLogger(kwargs.get('log_name', type(self).__name__))
        self.log.info("Engine init")



