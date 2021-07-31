
from typing import Any, Callable, Optional

from custom_components.script_engine.decorator.state import State
from custom_components.script_engine.hass.extension.state import StateExt

class IfState(State):
    """
    Decorator that checks if a state is valid
    """

    def __init__(self,
            id: str, 
            state: Optional[Any] = "*",
            bigger_than: Optional[Any] = "*",
            smaller_than: Optional[Any] = "*",
            custom_eval: Optional[Callable[[Any ,Any], bool]] = None,
            stay_valid: Optional[bool] = False,
            *args, **kwargs):
        super().__init__(id, state=state, previous_state="*", bigger_than=bigger_than, smaller_than=smaller_than, custom_eval=custom_eval, *args, **kwargs)

        self.decorator_type = "IfState"
        self.name = type(self).__name__

        self.stay_valid = stay_valid

    def setup(self, *args, **kwargs):
        self.new_state = None

        return super().setup(*args, **kwargs)

    def get_default_output(self, *args, **kwargs):  # overwrite base method
        state = kwargs.get("states", [])
        state.append(self.new_state)
        kwargs["states"] = state
        return args, kwargs

    def default(self, *args, **kwargs):

        def update():
            self.new_state = StateExt.get_state(self.hass, self.id).state
            self.valid = self.is_valid(self.new_state, old_state=None)

        if not self.stay_valid or (self.stay_valid and not self.valid):
            update()

        return super().default(*args, **kwargs)
