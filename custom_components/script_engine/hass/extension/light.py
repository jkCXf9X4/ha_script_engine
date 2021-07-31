import logging

from homeassistant.core import State

from .service import ServiceExt
from .state import StateExt

class LightExt:

    _logger = logging.getLogger(__name__)

    @classmethod
    def turn_on_light(cls, hass, id, data={}, debug=False):
        ServiceExt.call_service(hass, "light", "turn_on", id, data, debug)

    @classmethod
    def turn_off_light(cls, hass, id, data={}, debug=False):
        ServiceExt.call_service(hass, "light", "turn_off", id, data, debug)

    @classmethod
    def get_light_info(self, debug=False):
        state = StateExt.get_state(self.hass, self.id, debug)
        if state != None:
            on_off = state.state
            attributes = ["brightness", "color_temp", "rgb_color", "rgbw_color", "rgbww_color"]
            data = {}
            for i in attributes:
                if state.attributes.get(i, None) != None:
                    data[i] = state.attributes[i]
            return on_off, data
