
import datetime

from custom_components.script_engine.decorator import IfState
from custom_components.script_engine.engine import Engine

class _Script_Presence(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @IfState(id="group.family", state="home")
    def _script_is_home(self, *args, **kwargs):
        if kwargs.get('setup', False):
            # self.log.info("in setup script_1:scrpt_1")
            return True

        self.log.info("in main script_1:scrpt_1")

    @IfState(id="group.family", state="not_home")
    def _script_1(self, *args, **kwargs):
        if kwargs.get('setup', False):
            # self.log.info("in setup script_1:scrpt_1")
            return True

        self.log.info("in main script_1:scrpt_1")