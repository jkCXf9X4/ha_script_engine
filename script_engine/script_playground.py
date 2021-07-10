
import datetime

from custom_components.script_engine.decorator.if_state import IfState
from custom_components.script_engine.engine import Engine
from custom_components.script_engine.type.script_time import ScriptTime

class _Script_Playground(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    @IfState(id="input_boolean.is_home", state="off", debug=True)
    @IfState(id="group.family", state="home", debug=True)
    @IfState(id="sensor.time", bigger_than=ScriptTime("03:00"), debug=True)
    def _script_play_1(self, *args, **kwargs):
        if kwargs.get('setup', False):
            # self.log.info("in setup script_1:scrpt_1")
            return True

        self.log.info("Play_1 triggered")

    @IfState(id="group.family", state="not_home")
    def _script_play_2(self, *args, **kwargs):
        if kwargs.get('setup', False):
            # self.log.info("in setup script_1:scrpt_1")
            return True

        self.log.info("Play:2 triggered")
