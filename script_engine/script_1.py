from engine import Engine

class script_1(Engine):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log.info("Init hase_1")

    @Engine.event_decorator
    def script_turn_on_ligt(self):
        self.log.info("turn on ligt hase_1")

