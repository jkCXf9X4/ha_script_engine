
from custom_components.script_engine.engine import Engine, DOMAIN
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguents
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap

class _Script_LightSensorOutside(Engine):

    light_outside_id = f"{DOMAIN}.light_outside"
    light_sensor_id = "sensor.lumi_lumi_sen_ill_mgl01_8b21773c_illuminance"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @Duality()
    @ToState(id=light_sensor_id, bigger_than=1000.0)
    def _script_light_outside(self, *args, **kwargs):

        condition = kwargs.get("condition")
        if condition:
            StateExt.set_state(self.hass, self.light_outside_id, True)
        else:
            StateExt.set_state(self.hass, self.light_outside_id, False)
