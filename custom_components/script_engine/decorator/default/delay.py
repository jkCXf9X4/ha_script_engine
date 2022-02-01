
from custom_components.script_engine.decorator.default.to_state import ToState
import datetime

from custom_components.script_engine.type.script_datetime import ScriptDateTime

class Delay(ToState):
    '''
    Adds a start delay after home assistant is started
    '''

    @staticmethod
    def delay(minutes):
        start_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        return ScriptDateTime(start_time.isoformat())

    def __init__(self, minutes=1, *args, **kwargs):
        super().__init__(id="sensor.date_time_iso", bigger_than=self.delay(minutes), stay_valid=True, *args, **kwargs)
