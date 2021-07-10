
import datetime

from custom_components.script_engine.decorator.if_state import IfState
from custom_components.script_engine.engine import Engine
from custom_components.script_engine.type.script_time import ScriptTime


def timeplus2():
    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=2)
    # delta = datetime.datetime(minute=2)

    t = now + delta
    t = t.time().strftime("%H:%M")
    return ScriptTime(t)

class _Script_Time(Engine):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @IfState(id="group.family", state="home")
    @IfState(id="sensor.time", state="22:00")
    @IfState(id="binary_sensor.workday_sensor", state="on")
    def _script_bedtime_workday(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("home_status", "sleep")

    @IfState(id="group.family", state="home")
    @IfState(id="sensor.time", state="23:00")
    @IfState(id="binary_sensor.workday_sensor", state="off")
    def _script_bedtime_weekend(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("home_status", "sleep")

    @IfState(id="group.family", state="home")
    @IfState(id="sensor.time", state="06:00")
    @IfState(id="binary_sensor.workday_sensor", state="on")
    def _script_morning_workday(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("home_status", "awake")

    @IfState(id="group.family", state="home")
    @IfState(id="sensor.time", state="08:00")
    @IfState(id="binary_sensor.workday_sensor", state="off")
    def _script_morning_weekend(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("home_status", "awake")

    @IfState(id="group.family", state="not_home")
    def _script_away(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return True

        self.set_local_state("home_status", "away")
