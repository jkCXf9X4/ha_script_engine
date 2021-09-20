
import logging
from typing import List

from custom_components.script_engine.hass.extension import StateExt

from .light import LightWrap

class LightGroupWrap:
    def __init__(self, hass, group_id, debug=False) -> None:
        self.hass = hass
        self.group_id = group_id

        self.light_ids = None
        self.lights = None

        self.debug = debug

        self.log = logging.getLogger(__name__)

    def setup(self): # late setup required since light groups gets populated late at startup
        if self.light_ids == None:
            self.light_ids: List = StateExt.get_ids_from_group(self.hass, self.group_id)
            not self.debug or self.log.debug(f"Group Ids {self.light_ids}")
        if self.lights == None:
            self.lights = [LightWrap(self.hass, i, debug=self.debug) for i in self.light_ids]
            not self.debug or self.log.debug(f"Group lights { [str(i) for i in self.lights]}")

    def turn_on(self, data={}):
        if self.lights != None:
            _ = [i.turn_on(data=data) for i in self.lights]
        else:
            not self.debug or self.log.debug(f"Group id {self.group_id}, turn_on fallthru, no action")

    def turn_off(self, save_state=True):
        if self.lights != None:
            _ = [i.turn_off(save_state=save_state) for i in self.lights]
        else:
            not self.debug or self.log.debug(f"Group id {self.group_id}, turn_off fallthru, no action")

    def restore(self, data={}):
        if self.lights != None:
            _ = [i.restore(data=data) for i in self.lights]
        else:
            not self.debug or self.log.debug(f"Group id {self.group_id}, restore fallthru, no action")

    def __str__(self) -> str:
        return [str(i) for i in self.lights]
