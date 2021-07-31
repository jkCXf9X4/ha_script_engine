
import datetime

from custom_components.script_engine.engine import Engine, DOMAIN
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguents
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap

from custom_components.script_engine.type.script_time import ScriptTime


class _Script_HomeStatus(Engine):

    home_status_id = f"{DOMAIN}.home_status"
    sleep = "sleep"
    awake = "awake"
    away = "away"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @ToState(id="group.family", state="home")
    @ToState(id="sensor.time", state="22:00")
    @ToState(id="binary_sensor.workday_sensor", state="on")
    def _script_bedtime_workday(self, *args, **kwargs):

        StateExt.set_state(self.hass, self.home_status_id, self.sleep)

    @ToState(id="group.family", state="home")
    @ToState(id="sensor.time", state="23:00")
    @ToState(id="binary_sensor.workday_sensor", state="off")
    def _script_bedtime_weekend(self, *args, **kwargs):

        StateExt.set_state(self.hass, self.home_status_id, self.sleep)

    @ToState(id="group.family", state="home")
    @ToState(id="sensor.time", state="06:00")
    @ToState(id="binary_sensor.workday_sensor", state="on")
    def _script_morning_workday(self, *args, **kwargs):

        StateExt.set_state(self.hass, self.home_status_id, self.awake)

    @ToState(id="group.family", state="home")
    @ToState(id="sensor.time", state="08:00")
    @ToState(id="binary_sensor.workday_sensor", state="off")
    def _script_morning_weekend(self, *args, **kwargs):

        StateExt.set_state(self.hass, self.home_status_id, self.awake)

    @ToState(id="group.family", state="not_home")
    def _script_away(self, *args, **kwargs):

        StateExt.set_state(self.hass, self.home_status_id, self.away)
