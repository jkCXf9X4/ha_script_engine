import logging

class hase_1(Engine):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self._LOGGER = logging.getLogger(type(self).__name__)

        self.log.info("Init hase_1")

    @Engine.event_decorator
    def turn_on_ligt(self):
        self.log.info("turn on ligt hase_1")

