
from typing import Any, Callable, Optional

from custom_components.script_engine.decorator.abc.state import State
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
            custom_eval_condition: Optional[Any] = True,
            persistent: Optional[bool] = False,
            init_valid_state: Optional[bool] = False,
            *args, **kwargs):

        super().__init__(id,
            state=state,
            previous_state="*",
            bigger_than=bigger_than,
            smaller_than=smaller_than,
            custom_eval=custom_eval,
            custom_eval_condition=custom_eval_condition,
            persistent=persistent,
            init_valid_state=init_valid_state
            *args, **kwargs)

    def execute(self, *args, **kwargs):
        self.new_event_state = self.hass.states.get(self.id)

        state = kwargs.get("states", [])
        state.append(self.new_event_state)
        kwargs["states"] = state

        self.update_state()
        kwargs["result"][self.handler.get_index(self)] = self.state

        return super().execute(*args, **kwargs)
