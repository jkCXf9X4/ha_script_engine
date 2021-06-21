
import logging

#TODO: import
from test_class import Test_class 

class script_2(Engine):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.t = Test_class()

        self.log.info("Init hase_2")

    def script_turn_on_ligt(self):
        self.log.info("turn on ligt hase_2")

