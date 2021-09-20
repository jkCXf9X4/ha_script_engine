import datetime as dt

class SimpleTime:
    """
    Time class that can be added and subtracted

    All operands return a new SimpleTime
    """

    seconds_per_minute = 60
    minutes_per_hour = 60
    hours_per_day = 24
    seconds_per_hour = seconds_per_minute * minutes_per_hour
    seconds_per_day = seconds_per_hour * hours_per_day

    @classmethod
    def get_seconds(cls, hours=0, minutes=0, seconds=0):
        return hours * cls.seconds_per_hour + minutes * cls.seconds_per_minute + seconds

    def __init__(self, hours=0, minutes=0, seconds=0) -> None:
        self._total_seconds = 0
        self.total_seconds = self.get_seconds(hours=hours, minutes=minutes, seconds=seconds)

    def to_time(self) -> dt.time:
        return dt.time(hour=self.hour, minute=self.minute, second=self.second)

    def to_datetime(self) -> dt.datetime:
        """
        Get current date with time from simple time
        """
        now = dt.datetime.now()
        return dt.datetime(now.year, now.month, now.day, hour=self.hour, minute=self.minute, second=self.second)

    def to_timedelta(self) -> dt.timedelta:
        return dt.timedelta(seconds=self.total_seconds)

    @classmethod
    def now(cls):
        now = dt.datetime.now()
        return cls(hours=now.hour, minutes=now.minute, seconds=now.second)

    @staticmethod
    def is_between(a, b, c):
        """ 
        Check if a <= b <= c is valid
        """
        if a >= c:
            return ( b >= a or b <= c)
        elif c >= a:
            return a <= b <= c
        else:
            return False

    @property
    def total_seconds(self):
        return self._total_seconds

    @total_seconds.setter
    def total_seconds(self, var):
        self._total_seconds = var % self.seconds_per_day

    @property
    def hour(self):
        return self.total_seconds // self.seconds_per_hour

    @property
    def minute(self):
        return (self.total_seconds // 60) % 60

    @property
    def second(self):
        return self.total_seconds % self.seconds_per_minute

    def __str__(self):
        return self.to_time().strftime("%H:%M")

    def __hash__(self):
        return hash(self.total_seconds)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.total_seconds == other.total_seconds

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.total_seconds != other.total_seconds

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.total_seconds < other.total_seconds

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.total_seconds <= other.total_seconds

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.total_seconds > other.total_seconds

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.total_seconds >= other.total_seconds

    def __add__(self, other):
        seconds = 0
        if isinstance(other, self.__class__):
            seconds = self.total_seconds + other.total_seconds
        elif isinstance(other, dt.timedelta):
            seconds = self.total_seconds + other.total_seconds()
        else:
            return NotImplemented

        return self.__class__(seconds=seconds)

    def __sub__(self, other):
        seconds = 0
        if isinstance(other, self.__class__):
            seconds = self.total_seconds - other.total_seconds
        elif isinstance(other, dt.timedelta):
            seconds = self.total_seconds - other.total_seconds()
        else:
            return NotImplemented

        if seconds < 0:
            seconds = self.seconds_per_day + seconds
        return self.__class__(seconds=seconds)
