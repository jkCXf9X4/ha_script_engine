
from typing import List

from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguments, IfState, Delay
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap
from custom_components.script_engine.const import DOMAIN

from script_engine.script_time import _Script_HomeStatus
from script_engine.script_light_sensor import _Script_LightSensorOutside

class _Script_Locks(Engine):

    UNLOCKED = "unlocked"
    LOCKED = "locked"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.locks = ["lock.back", "lock.main", "lock.carport"]

    def lock(self, id):
        state = self.hass.states.get(id)
        if state != self.LOCKED:
            # pass
            self.hass.services.call("lock", "lock", target= {"entity_id" : id})

    @Delay(minutes=2)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.sleep)
    def _script_lock_doors(self, *args, **kwargs):
        self.log.info("Lock doors")
        _ = [self.lock(i)  for i in self.locks]

    @Delay(minutes=2)
    @ToState(id=_Script_HomeStatus.home_status_id, state=_Script_HomeStatus.away)
    def _script_lock_doors_2(self, *args, **kwargs):
        self.log.info("Lock doors")
        _ = [self.lock(i)  for i in self.locks]
