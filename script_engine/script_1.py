

class script_1(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log.info("Init hase_1")

    @AtStateChange(id="input_boolean.is_home", to_state="off")
    def script_turn_on_ligt(self, *args, **kwargs):
        self.log.info("in turn on ligt hase_1")
        if kwargs.get('is_setup', False):
            self.log.info("in setup turn on ligt hase_1")
            return

        self.log.info("turn on ligt hase_1")
