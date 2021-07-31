import datetime as dt
import time

from custom_components.script_engine.type.simple_time import SimpleTime

class ScriptTime(SimpleTime):

    def __init__(self, hours=0, minutes=0, seconds=0) -> None:
        """
        Variable hours can be a timestring with format "12:00" to ensure that the conversion from home assistent is correct
        """
        if type(hours) == str:
            t = dt.datetime.strptime(hours, "%H:%M").time()
            hours, minutes, seconds = (t.hour, t.minute, t.second,)
        print(hours, minutes, seconds)
        super().__init__(hours=hours, minutes=minutes, seconds=seconds)
