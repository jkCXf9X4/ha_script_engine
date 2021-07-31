import datetime

from custom_components.script_engine.type.script_datetime import ScriptDateTime
from custom_components.script_engine.decorator.if_state import IfState

class Delay(IfState):
    '''
    Adds a start delay after home assistant is started
    '''

    @staticmethod
    def delay(minutes):
        now = datetime.datetime.now()
        delta = datetime.timedelta(minutes=minutes)

        t = now + delta
        t = t.isoformat()
        return ScriptDateTime(t)

    def __init__(self, minutes=1):
        super().__init__(id, bigger_than=self.delay(minutes), stay_valid=True)
