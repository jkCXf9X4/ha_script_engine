# from engine import Engine

from test_class import Test_class

class script_2(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log.info("Init hase_2")

        self.t = Test_class()

        self.log.info(self.t.get_stuff())

    def script_turn_on_light_2(self, *args, **kwargs):
        if kwargs.get('setup', False):
            self.log.info("in setup turn on ligt hase_2")
            return True

        self.log.info("turn on ligt hase_2")

