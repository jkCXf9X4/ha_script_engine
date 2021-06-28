
class script_1(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log.info("Init hase_1")

    @ToState(id="input_boolean.is_home", to_state="off", from_state="*")
    def script_turn_on_light_1(self, *args, **kwargs):
        if kwargs.get('setup', False):
            self.log.info("in setup turn on ligt hase_1")
            return True

        self.log.info("turn on ligt hase_1")
