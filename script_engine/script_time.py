
from custom_components.script_engine.decorator.delay import Delay
import datetime

from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguments
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap
from custom_components.script_engine.const import DOMAIN

from custom_components.script_engine.type.script_time import ScriptTime


class _Script_HomeStatus(Engine):

    home_status_id = f"{DOMAIN}.home_status"
    sleep = "sleep"
    awake = "awake"
    away = "away"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def sleep_time():
        now = datetime.datetime.now()
        weekday = now.weekday()

        if weekday in [6, 0, 1, 2, 3]:
            return ScriptTime("21:00")
        else:
            return ScriptTime("22:00")

    def wake_up_time():
        now = datetime.datetime.now()
        weekday = now.weekday()

        if weekday in [0, 1, 2, 3, 4]:
            return ScriptTime("06:00")
        else:
            return ScriptTime("7:30")

    @Delay(1)
    @ToState(id="group.family", state="home")
    @ToState(id="sensor.time", bigger_than=sleep_time, smaller_than=wake_up_time)
    def _script_bedtime(self, *args, **kwargs):
        self.log.debug("Family is sleeping")
        self.hass.states.async_set(entity_id=self.home_status_id, new_state=self.sleep)

    @Delay(1)
    @ToState(id="group.family", state="home")
    @ToState(id="sensor.time", bigger_than=wake_up_time, smaller_than=sleep_time)
    def _script_morning(self, *args, **kwargs):
        self.log.debug("Family is awake")
        self.hass.states.async_set(entity_id=self.home_status_id, new_state=self.awake)

    @Delay(1)
    @ToState(id="group.family", state="not_home")
    def _script_away(self, *args, **kwargs):
        self.log.debug("Family is away")
        self.hass.states.async_set(entity_id=self.home_status_id, new_state=self.away)
