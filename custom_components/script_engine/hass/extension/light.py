import logging

from homeassistant.core import HomeAssistant, State

from .service import ServiceExt
from .state import StateExt

class LightExt:

    _logger = logging.getLogger(__name__)

    ON_STATE = "on"
    OFF_STATE = "off"
    UNKNOWN_STATE = ""

    @classmethod
    def turn_on(cls, hass : HomeAssistant, id, data={}, debug=False):
        ServiceExt.call_service(hass,"light" , "turn_on", service_data=data, target= {"entity_id" : id}, debug=debug)
        # hass.services.call("light", "turn_on", service_data=data, target= {"entity_id" : id})

    @classmethod
    def turn_off(cls, hass: HomeAssistant, id, data={}, debug=False):
        ServiceExt.call_service(hass,"light" , "turn_off", service_data=data, target= {"entity_id" : id}, debug=debug)
        # hass.services.call("light", "turn_off", service_data=data, target= {"entity_id" : id})

    @classmethod
    def get_std_attributes(cls, hass :HomeAssistant, id, debug=False):
        state = hass.states.get(id)
        if state == None:
            raise Exception(f"Exception, {id} state not existing")
        else:
            on_off = state.state
            attributes = ["brightness", "color_temp", "rgb_color", "rgbw_color", "rgbww_color"]
            data = {}
            for i in attributes:
                if state.attributes.get(i, None) != None:
                    data[i] = state.attributes[i]
            return on_off, data
        