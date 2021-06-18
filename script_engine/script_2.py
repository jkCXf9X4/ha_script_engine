
import logging

class script_2(Engine):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log.info("Init hase_2")

    def script_turn_on_ligt(self):
        self.log.info("turn on ligt hase_2")

