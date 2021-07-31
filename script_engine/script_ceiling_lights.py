
from typing import List

from custom_components.script_engine.engine import Engine, DOMAIN
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguents, IfState
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap

from .script_time import _Script_HomeStatus
from .script_light_sensor import _Script_LightSensorOutside

class _Script_CeilingLights(Engine):

    group_id = "group.ceiling_lamps"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.light_ids: List = StateExt.get_ids_from_group(self.hass, self.group_id)
        self.log.debug(self.light_ids)

        self.lights = [LightWrap(i) for i in self.light_ids]

    @ToState(id=group_id, state="**", debug=True)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.awake)
    @ToState(id=_Script_LightSensorOutside.light_outside_id, state=True)
    def _script_turn_off_ceiling_lights(self, *args, **kwargs):

        self.log.info("Turn off ceiling lights")
        _ = [i.turn_off() for i in self.lights]

    @ToState(id=group_id, state="**", debug=True)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.awake)
    @ToState(id=_Script_LightSensorOutside.light_outside_id, state=False)
    def _script_turn_on_ceiling_lights(self, *args, **kwargs):

        self.log.info("Turn on ceiling lights")
        _ = [i.turn_on() for i in self.lights]
