from datetime import datetime, timedelta

class ScriptDateTime(datetime):
    """
    Use with sensor.date_time_iso from https://www.home-assistant.io/integrations/time_date/
    """

    def __new__(cls, str):
        d = datetime.fromisoformat(str)
        return super().__new__(cls, d.year, d.month, d.day, hour=d.hour, minute=d.minute, second=d.second, microsecond=d.microsecond)

    def to_datetime(self):
        return datetime(self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond, self.tzinfo)

    def __str__(self) -> str:
        return self.isoformat()

    def __add__(self, other: timedelta):
        i = self.to_datetime() + other
        j = ScriptDateTime(str(i))
        return j

    def __sub__(self, other: timedelta):
        i = self.to_datetime() - other
        j = ScriptDateTime(str(i))
        return j
