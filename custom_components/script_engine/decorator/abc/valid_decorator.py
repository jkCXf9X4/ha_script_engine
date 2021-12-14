
import datetime
from enum import Enum
from custom_components.script_engine.decorator.decorator_type import DecoratorType
from custom_components.script_engine.decorator.abc.decorator import Decorator
    
class ValidDecorator(Decorator):

    def __init__(self, init_valid_state = False, persistent = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_valid_state = init_valid_state
        self.state = init_valid_state
        self.previous_state = init_valid_state
    
        self.state_switch_time: datetime.datetime = None

        self.persistent = persistent
        self.type = DecoratorType.BOOLEAN

    def update_state(self):
        not self.debug or self.log.debug(f"update, pre: {self}")
        if not self.persistent or (self.persistent and self.init_valid_state == self.state):
            self.previous_state = self.state
            self.state = self.validate()
            not self.debug or self.log.debug(f"update, after: {self}")

            if self.previous_state is not self.state:
                self.state_switch_time = datetime.datetime.now()            
    
    def validate(self) -> bool:
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"{self.name}:{self.type}:wrap's {self.function.get_name()}, state: {self.state}"