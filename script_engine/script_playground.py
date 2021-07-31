
from custom_components.script_engine.engine import Engine, DOMAIN
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguents, IfState
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap

from .script_time import ScriptTime

class _Script_Playground(Engine):

    id = f"{DOMAIN}.playground_id"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @ToState(id="lock.main", state="unlocked")
    @ToState(id="sensor.time", bigger_than=ScriptTime("16:00"))
    @IfState(id="group.family", state="home")
    def _script_play_1(self, *args, **kwargs):

        StateExt.set_state(self.hass, self.id, "State_1")

    @Debug()  # Observ brackets
    @Duality()  # Observ brackets
    @ToState(id="input_boolean.is_home", state="on", debug=False)
    def _script_play_2(self, *args, **kwargs):

        condition = kwargs.get("condition")
        if condition:
            LightExt.turn_on_light(self.hass, id="light.hunden_on_off", data={})
        else:
            LightExt.turn_off_light(self.hass, id="light.hunden_on_off", data={})
