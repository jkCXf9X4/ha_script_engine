
import logging
from typing import List

from custom_components.script_engine.hass.extension import StateExt
from custom_components.script_engine.hass.extension import LightExt
class LightWrap:
    def __init__(self, hass, id, debug=False) -> None:
        self.hass = hass
        self.id = id
        self.state = None
        self.data = {}
        self.debug = debug

        self.log = logging.getLogger(__name__)

    def turn_off(self, save_state=True):
        if save_state:
            not self.debug or self.log.debug(f"Light {self.id}, saving state")
            try:
                self.state, self.data = LightExt.get_std_attributes(self.hass, self.id)
                not self.debug or self.log.debug(f"State: {self.state}, Data: {self.data}")
            except Exception:
                not self.debug or self.log.debug(f"Exception: Unable to save state")
                not self.debug or self.log.debug(f"State: {self.state}, Data: {self.data}")
        LightExt.turn_off(self.hass, self.id, debug=self.debug)

    def turn_on(self):
        not self.debug or self.log.debug(f"Light {self.id}, turning on")
        state = StateExt.get_state(self.hass, self.id, debug=self.debug).state
        if state != LightExt.ON_STATE:
            LightExt.turn_on(self.hass, self.id, debug=self.debug)

    def restore(self):
        if self.data != {}:
            not self.debug or self.log.debug(f"Light {self.id}, restore, restoring state")
            not self.debug or self.log.debug(f"State: {self.state}, Data: {self.data}")
            LightExt.turn_on(self.hass, self.id, data=self.data, debug=self.debug)
        else:
            not self.debug or self.log.debug(f"Light {self.id}, restore, missing data, only turning on")
            LightExt.turn_on(self.hass, self.id, debug=self.debug)

    def __str__(self) -> str:
        return f"LightWrap_{self.id}_{self.state}_{self.data}"
