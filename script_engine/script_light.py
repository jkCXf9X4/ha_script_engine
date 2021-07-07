
import datetime

from custom_components.script_engine.decorator import IfState
from custom_components.script_engine.engine import Engine

class _Script_Light(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @IfState(id="sensor.lumi_lumi_sen_ill_mgl01_8b21773c_illuminance", previous_state="**", bigger_than=1000.0)
    def script_light_outside(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_state("binary_sensor.light_outside", True)

    @IfState(id="sensor.lumi_lumi_sen_ill_mgl01_8b21773c_illuminance", previous_state="**", smaller_than=1000.0)
    def script_dark_outside(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_state("binary_sensor.light_outside", False)
