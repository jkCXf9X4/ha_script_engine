
from datetime import datetime, timedelta, timezone
from logging import fatal
from custom_components.script_engine.decorator.abc.valid_decorator import ValidDecorator

from custom_components.script_engine.decorator.abc.decorator import Decorator
from custom_components.script_engine.decorator.decorator_type import DecoratorType

class Proximity(ValidDecorator):
    """
    Decorator that ensures that a function can not be called to closely again
    """
    def __init__(self, hours=0, minutes=1,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hours = hours
        self.minutes = minutes

    def time_is_outside_proximity(self):
        return (self.state_switch_time + timedelta(hours=self.hours, minutes=self.minutes)) < datetime.now(timezone.utc)

    def validate(self) -> bool:
        if self.state_switch_time == None or self.time_is_outside_proximity():
            return True
        return False

    def execute(self, *args, **kwargs):
        self.update_state()
        kwargs["result"][self.handler.get_index(self)] = self.state

        return super().execute(*args, **kwargs)