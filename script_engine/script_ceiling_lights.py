
from typing import List

from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguments, IfState , Delay
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap, LightGroupWrap
from custom_components.script_engine.const import DOMAIN

from script_engine.script_time import _Script_HomeStatus
from script_engine.script_light_sensor import _Script_LightSensorOutside

class _Script_CeilingLights(Engine):

    group_id = "group.ceiling_lamps"
    group_exists_id = f"{DOMAIN}.ceiling_lights_exists"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.light_group = LightGroupWrap(self.hass, self.group_id)

    # The light group is not existing from the start and any use must wait until it exists
    @Delay(minutes=1)
    @ToState(id=group_id, state="**")
    def _script_init_group_lights(self, *args, **kwargs):
        self.log.debug("Setting up ceiling lights")
        self.light_group.setup()
        self.hass.states.async_set(entity_id=self.group_exists_id, new_state=True)

    @ToState(id=group_exists_id, state=True)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.awake)
    @ToState(id=_Script_LightSensorOutside.light_outside_id, state=False)
    def _script_turn_on_ceiling_lights(self, *args, **kwargs):
        self.log.info("Turn on ceiling lights")
        self.light_group.restore()

    @ToState(id=group_exists_id, state=True)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.awake)
    @ToState(id=_Script_LightSensorOutside.light_outside_id, state=True)
    def _script_turn_off_ceiling_lights(self, *args, **kwargs):
        self.log.info("Turn off ceiling lights")
        self.light_group.turn_off()

    @ToState(id=group_exists_id, state=True)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.sleep)
    def _script_turn_off_ceiling_lights(self, *args, **kwargs):
        self.log.info("Turn off ceiling lights")
        self.light_group.turn_off()

    @ToState(id=group_exists_id, state=True)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.away)
    def _script_turn_off_ceiling_lights(self, *args, **kwargs):
        self.log.info("Turn off ceiling lights")
        self.light_group.turn_off()


