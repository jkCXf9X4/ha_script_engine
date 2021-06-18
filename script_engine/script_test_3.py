import logging

class script_test_3(Engine):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log.info("Init hase_test")

    @Engine.event_decorator
    def script_turn_on_ligt(self):
        self.log.info("turn on ligt hase_test")