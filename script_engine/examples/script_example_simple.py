
from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState

class _Script_ExampleSimple(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @ToState(id="group.family", state="home")
    def _script_is_home(self, *args, **kwargs):
        self.log.info("Someone is home")

    @ToState(id="group.family", state="not_home")
    def _script_is_away(self, *args, **kwargs):
        self.log.info("No one is home")
