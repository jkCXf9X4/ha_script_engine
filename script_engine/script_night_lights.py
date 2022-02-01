
from typing import List

from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguments, IfState, Delay
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap, LightGroupWrap
from custom_components.script_engine.const import DOMAIN

from script_engine.script_light_sensor import _Script_LightSensorOutside

from homeassistant.core import callback

class _Script_NightLights(Engine):

    group_id = "group.night_lamps"
        
    @Delay(1)
    @ToState(id=_Script_LightSensorOutside.light_outside_id, state=False)
    def _script_turn_on_night_lights(self, *args, **kwargs):
        self.log.debug("Turn on night lights")
        self.hass.services.call("homeassistant", "turn_on", target= {"entity_id" : self.group_id})

    @Delay(1)
    @ToState(id=_Script_LightSensorOutside.light_outside_id, state=True)
    def _script_turn_off_night_lights(self, *args, **kwargs):
        self.log.debug("Turn off night lights")
        self.hass.services.call("homeassistant", "turn_off", target= {"entity_id" : self.group_id})
