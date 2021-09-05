
from datetime import datetime, timedelta, timezone
import statistics
from typing import List

from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguments, Delay, Proximity
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap
from custom_components.script_engine.const import DOMAIN

from homeassistant.core import State


class _Script_LightSensorOutside(Engine):

    light_outside_id = f"{DOMAIN}.light_outside"
    light_sensor_id = "sensor.lumi_lumi_sen_ill_mgl01_8b21773c_illuminance"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.hass.states.async_set(entity_id=self.light_outside_id, new_state='False')
        self.light_states: List[State] = []

    def custom(self, new_state: State, old_state: State) -> bool:
        """
        Calculate and compare the mean over a set time period
        """
        not self.debug or self.log.info(f"--- Custom eval light ---")
        def time_inside_frame_from_timeframe_to_now(dt: datetime, hours=0, minutes=0):
            if (datetime.now(timezone.utc) - timedelta(hours=hours, minutes=minutes)) < dt:
                return True
            else:
                return False

        # can be called from multiple functions this causing double entries
        if new_state not in self.light_states:
            self.light_states.append(new_state)

        self.light_states = [i for i in self.light_states if time_inside_frame_from_timeframe_to_now(i.last_changed, minutes=15)]
        values = [float(i.state) for i in self.light_states]
        mean = statistics.mean(values)
        # not self.debug or self.log.info(f"states: {self.light_states}")
        not self.debug or self.log.info(f"Mean {mean}, len {len(values)}, values: {values}")

        if mean >= 150.0:
            not self.debug or self.log.info(f"return True")
            return True

        not self.debug or self.log.info(f"return False")
        return False

    @ToState(id=light_sensor_id, custom_eval=custom)
    @Proximity(minutes=30)
    def _script_light_outside(self, *args, **kwargs):
        self.log.info(f"Its light outside")
        self.hass.states.async_set(entity_id=self.light_outside_id, new_state=True)

    @ToState(id=light_sensor_id, custom_eval=custom, custom_eval_condition=False)
    @Proximity(minutes=30)
    def _script_dark_outside(self, *args, **kwargs):
        self.log.info(f"Its dark outside")
        self.hass.states.async_set(entity_id=self.light_outside_id, new_state=False)
