from custom_components.script_engine.type.script_time import ScriptTime
import datetime
from typing import List

from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguments, IfState , Delay
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap, LightGroupWrap
from custom_components.script_engine.const import DOMAIN

from script_engine.script_time import _Script_HomeStatus
from script_engine.script_light_sensor import _Script_LightSensorOutside

from homeassistant.core import State

class _Script_CeilingLights(Engine):

    group_id = "group.ceiling_lamps"
    group_exists_id = f"{DOMAIN}.ceiling_lights_exists"
    
    light_bedroom_id = "light.dimmer_sovrum_light"

    # The light group is not existing from the start and any use must wait until it exists
    @Delay(minutes=2)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.awake)
    @ToState(id=_Script_LightSensorOutside.light_outside_id, state=False)
    def _script_turn_on_ceiling_lights(self, *args, **kwargs):
        self.log.info("Turn on ceiling lights")
        self.hass.services.call("homeassistant", "turn_on", target= {"entity_id" : self.group_id})

    @Delay(minutes=2)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.awake)
    @ToState(id=_Script_LightSensorOutside.light_outside_id, state=True)
    def _script_turn_off_ceiling_lights_1(self, *args, **kwargs):
        self.log.info("_script_turn_off_ceiling_lights_1")
        self.hass.services.call("homeassistant", "turn_off", target= {"entity_id" : self.group_id})

    @Delay(minutes=2)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.sleep)
    def _script_turn_off_ceiling_lights_2(self, *args, **kwargs):
        self.log.info("_script_turn_off_ceiling_lights_2")
        self.hass.services.call("homeassistant", "turn_off", target= {"entity_id" : self.group_id})

    @Delay(minutes=2)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.away)
    def _script_turn_off_ceiling_lights_3(self, *args, **kwargs):
        self.log.info("_script_turn_off_ceiling_lights_2")
        self.hass.services.call("homeassistant", "turn_off", target= {"entity_id" : self.group_id})


    def custom_eval_bedroom_plug(self, new:  State, old : State):
        brightness = new.attributes.get("brightness", 0)
        if brightness == None:
            # When turning off the brightness wont exist
            return False
    
        if brightness > 100:
            return True
        else:
            return False

    def inverted_custom_eval_bedroom_plug(self, new, old):
        return not self.custom_eval_bedroom_plug(new, old)      

    @Delay(minutes=2)
    @Debug()
    @ToState(id=light_bedroom_id, custom_eval=custom_eval_bedroom_plug )
    def _script_turn_on_bedroom_plug(self, *args, **kwargs):
        self.log.info("_script_turn_on_bedroom_plug, on")
        self.hass.services.call("homeassistant", "turn_on", target= {"entity_id" : "light.p6"})
        
    @Delay(minutes=2)
    @Debug()
    @ToState(id=light_bedroom_id, custom_eval=inverted_custom_eval_bedroom_plug)
    def _script_turn_off_bedroom_plug(self, *args, **kwargs):
        self.log.info("_script_turn_on_bedroom_plug, off")
        self.hass.services.call("homeassistant", "turn_off", target= {"entity_id" : "light.p6"})

