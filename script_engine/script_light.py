
import datetime

from custom_components.script_engine.decorator.if_state import IfState
from custom_components.script_engine.engine import Engine

from custom_components.script_engine.const import DOMAIN

class _Script_Light(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @IfState(id="sensor.lumi_lumi_sen_ill_mgl01_8b21773c_illuminance", bigger_than=1000.0)
    def _script_light_outside(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("light_outside", True)

    @IfState(id="sensor.lumi_lumi_sen_ill_mgl01_8b21773c_illuminance", smaller_than=1000.0)
    def _script_dark_outside(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("light_outside", False)


    @IfState(id=Engine.get_local_id("home_status"), state="awake")
    @IfState(id=Engine.get_local_id("light_outside"), state=True)
    def _script_light_outside(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("light_outside", True)

    @IfState(id=Engine.get_local_id("home_status"), state="awake")
    @IfState(id=Engine.get_local_id("light_outside"), state=False)
    def _script_dark_outside(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("light_outside", False)