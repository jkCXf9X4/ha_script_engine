
from typing import Any, Callable, Optional

from custom_components.script_engine.event.event_distributor import EventDistributor
from custom_components.script_engine.event.event_wrapper import StateChangedEvent
from custom_components.script_engine.decorator.state import State

class ToState(State):
    """
    Decorator that is used to subscribe to and validate event states
    """

    def __init__(self,
            id: str, 
            state: Optional[Any] = "*",
            previous_state: Optional[Any] = "*",
            bigger_than: Optional[Any] = "*",
            smaller_than: Optional[Any] = "*",
            custom_eval: Optional[Callable[[Any ,Any], bool]] = None,
            custom_eval_condition: Optional[Any] = True,
            stay_valid: Optional[bool] = False,
            *args, **kwargs):

        super().__init__(id, state=state,
            previous_state=previous_state,
            bigger_than=bigger_than,
            smaller_than=smaller_than,
            custom_eval=custom_eval,
            custom_eval_condition=custom_eval_condition,
            stay_valid=stay_valid,
            *args, **kwargs)

        self.decorator_type = "IfState"
        self.name = type(self).__name__

        self.event_distributor = EventDistributor(self.hass, debug=self.debug)

    def setup(self, *args, **kwargs):
        self.event: StateChangedEvent = None
        self.previous_valid = None

        self.event_distributor.register_callback(self.id, callback=self.new_event)
        return super().setup(*args, **kwargs)

    def new_event(self, *args, **kwargs):
        """
        Extracts the states from the event, then consuming it to prevent any other decorator from using it

        Calls the first decorator and starts the walk down the decorator chain
        """
        self.event = kwargs.get("event", None)
        kwargs.pop("event", None)

        # Store which decorator is the event trigger
        kwargs["trigger"] = self

        self.new_state = self.event.new_state
        self.old_state = self.event.old_state

        not self.debug or self.log.debug(f"\n----New event----\nFunction: {self.get_wrapped_function_name()}, Decorator: {self.id} \nNew: {self.new_state}, Old: {self.old_state}")

        new_valid = self.is_valid(self.new_state, self.old_state)
        if new_valid != self.previous_valid:
            self.previous_valid = new_valid
            not self.debug or self.log.debug(f"A switch in state, proceding, new valid state: {new_valid}")

            self.decorators[0].default(*args, **kwargs)
        else:
            not self.debug or self.log.debug(f"No switch in state, aborting, state: {new_valid}")   

    def get_default_output(self, *args, **kwargs):
        events = kwargs.get("events", [])
        events.append(self.event)
        kwargs["events"] = events
        return args, kwargs

    def default(self, *args, **kwargs):
        not self.debug or self.log.debug(f"Default to_state: {self}")

        return super().default(*args, **kwargs)

    def teardown(self, *args, **kwargs):
        self.event_distributor.remove_callback(self.id, callback=self.new_event)
        return super().teardown(*args, **kwargs)
