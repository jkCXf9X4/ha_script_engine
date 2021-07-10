import datetime
import time

from custom_components.script_engine.type.string_init_type import StringInitType

class ScriptTime(StringInitType):

    @staticmethod
    def from_timedelta(dt: datetime.timedelta):
        new = ScriptTime(None)
        new.item = dt.seconds
        return new

    @staticmethod
    def time_in_range(start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def to_item(self, str):
        if str != None:
            t = time.strptime(str, "%H:%M")
            return datetime.timedelta(hours=t.tm_hour, minutes=t.tm_min).seconds
        return None

    def to_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self.item)

    def to_time(self) -> datetime.time:
        return datetime.time(hour=self.item // 3600, minute=(self.item // 60) % 60)

    def __str__(self):
        return self.to_time().strftime("%H:%M")

    def __add__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        i = self.to_timedelta() + other.to_timedelta()
        return ScriptTime.from_timedelta(i)

    def __sub__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        i = self.to_timedelta() - other.to_timedelta()
        return ScriptTime.from_timedelta(i)
