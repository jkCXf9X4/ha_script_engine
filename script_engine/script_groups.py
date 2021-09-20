
"""
Decalaration of groups 

Not used atm, using groups in hass(yaml)
"""

from typing import List

from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguments, IfState , Delay
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap, LightGroupWrap
from custom_components.script_engine.const import DOMAIN

from script_engine.script_time import _Script_HomeStatus
from script_engine.script_light_sensor import _Script_LightSensorOutside

class _Script_Groups(Engine):

    CEILING_LIGHTS = []
    NIGHT_LIGHTS = []
    LOCKS = ["lock.back", "lock.main", "lock.carport"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        
    # @Delay(1)
    # def _script_add(self, *args, **kwargs):
    #     self.hass.services.async_call("group", "add", {"object_id":"Test_group", "name":"Test_group", "entities":self.LOCKS})
