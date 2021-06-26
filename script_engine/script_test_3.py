
# from engine import Engine

class script_test_3(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log.info("Init hase_test_3")

    def script_turn_on_ligt(self, *args, **kwargs):
        if kwargs.get('is_setup', False):
            return

        self.log.info("turn on ligt hase_test_3")