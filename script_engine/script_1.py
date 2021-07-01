
from custom_components.script_engine.decorator import IfState
from custom_components.script_engine.engine import Engine

class script_1(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    # @IfState(id="input_boolean.is_home", to_state="off")
    # def script_1(self, *args, **kwargs):
    #     if kwargs.get('setup', False):
    #         # self.log.info("in setup script_1:scrpt_1")
    #         return True

    #     self.log.info("in main script_1:scrpt_1")

    # @IfState(id="input_boolean.is_home", to_state="off")
    # @IfState(id="input_boolean.test", state="off")
    # def script_2(self, *args, **kwargs):
    #     if kwargs.get('setup', False):
    #         # self.log.info("in setup script_1:script_2")
    #         return True

        # self.log.info("in main script_1:scrpt_2")

    @IfState(id="sensor.lumi_lumi_sen_ill_mgl01_8b21773c_illuminance", bigger_than=1000.0)
    def script_light_outside(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_state("light_outside", True)
        self.log.info("Its light outside")

    @IfState(id="sensor.lumi_lumi_sen_ill_mgl01_8b21773c_illuminance", smaller_than=1000.0)
    def script_dark_outside(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_state("light_outside", False)
        self.log.info("Its dark outside")
