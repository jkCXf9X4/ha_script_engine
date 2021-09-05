
from datetime import datetime, timedelta, timezone

from custom_components.script_engine.decorator.base_decorator import BaseDecorator

class Proximity(BaseDecorator):
    """
    Decorator that ensures that a function can not be called to closely again
    """

    def __init__(self, hours=0, minutes=1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.decorator_type = "Proximity"
        self.name = type(self).__name__

        self.hours = hours
        self.minutes = minutes

        self.last_trigger = None

    def time_inside_frame_from_timeframe_to_now(dt: datetime, hours=0, minutes=0):
        if (datetime.now(timezone.utc) - timedelta(hours=hours, minutes=minutes)) < dt:
            return True
        else:
            return False

    def default(self, *args, **kwargs):

        if self.last_trigger == None or self.time_inside_frame_from_timeframe_to_now(datetime.now(), self.hours, self.minutes):

            self.last_trigger = datetime.now()
            not self.debug or self.log.debug(f"Proximity decorator is valid, continuing")
            return super().default(*args, **kwargs)

        not self.debug or self.log.debug(f"Proximity decorator is not valid, aborting")
        return False
