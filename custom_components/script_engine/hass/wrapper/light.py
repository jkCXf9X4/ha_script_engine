
import logging
from typing import List

from custom_components.script_engine.hass.extension import StateExt
from custom_components.script_engine.hass.extension import LightExt

class LightGroupWrap:
    def __init__(self, group_id, debug=False) -> None:
        self.group_id = group_id

        self.light_ids = None
        self.lights = None

        self.debug = debug

        self.log = logging.getLogger(__name__)

    def set_ids(self):
        if self.light_ids == None:
            self.light_ids: List = StateExt.get_ids_from_group(self.hass, self.group_id)
            not self.debug or self.log.debug(f"Group Ids {self.light_ids}")

    def set_lights(self):
        if self.lights == None:
            self.lights = [LightWrap(i) for i in self.light_ids]
            not self.debug or self.log.debug(f"Group Ids {self.lights}")

    def turn_on(self, restore_state=True):

        _ = [i.turn_on(restore=restore_state) for i in self.lights]

    def turn_off(self, save_state=True):

        _ = [i.turn_off(save_state=save_state) for i in self.lights]

    def __str__(self) -> str:
        return [str(i) for i in self.lights]


class LightWrap:
    def __init__(self, hass, id, debug=False) -> None:
        self.hass = hass
        self.id = id
        self.state = None
        self.data = None
        self.debug = debug

        self.log = logging.getLogger(__name__)

    def turn_off(self, save_state=True):
        if save_state:
            self.state, self.data = LightExt.get_light_info()
        LightExt.turn_off_light(self.hass, self.id)

    def turn_on(self, restore=True):
        if restore and self.data != {}:
            LightExt.turn_on_light(self.hass, self.id, data=self.data)
        else:
            LightExt.turn_on_light(self.hass, self.id)

    def __str__(self) -> str:
        return f"LightWrap_{self.id}_{self.state}_{self.data}"
