
from typing import Any, Callable, Optional
from custom_components.script_engine.decorator.decorator_type import DecoratorType

from custom_components.script_engine.event.event_distributor import EventDistributor
from custom_components.script_engine.event.event_wrapper import StateChangedEvent
from custom_components.script_engine.decorator.abc.state import State

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
            persistent: Optional[bool] = False,
            init_valid_state: Optional[bool] = False,
            *args, **kwargs):

        super().__init__(
            id=id,
            state=state,
            previous_state=previous_state,
            bigger_than=bigger_than,
            smaller_than=smaller_than,
            custom_eval=custom_eval,
            custom_eval_condition=custom_eval_condition,
            persistent=persistent,
            init_valid_state=init_valid_state
            *args, **kwargs)

        self.event_distributor = EventDistributor(self.hass, debug=self.debug)
        self.event: StateChangedEvent = None

    def setup(self, *args, **kwargs):
        self.event_distributor.register_callback(self.id, callback=self.new_event)

    def new_event(self, *args, **kwargs):
        """
        Extracts the states from the event, then consuming it to prevent any other decorator from using it

        Calls the first decorator and starts the walk down the decorator chain
        """
        self.event = kwargs.pop("event", None)

        # Store which decorator is the event trigger
        kwargs["trigger"] = self

        self.new_event_state = self.event.new_state
        self.old_event_state = self.event.old_state

        not self.debug or self.log.debug(f"\n----New event----: {self}")

        self.update_state()
        if self.state != self.previous_state:
            not self.debug or self.log.debug(f"A switch in state, proceding, new state: {self.state}")
            self.handler.run(*args, **kwargs)
        else:
            not self.debug or self.log.debug(f"No switch in state, aborting, state: {self.state}")   

    def execute(self, *args, **kwargs):
        not self.debug or self.log.debug(f"execute: kwargs {kwargs}")

        events = kwargs.get("events", [])
        events.append(self.event)
        kwargs["events"] = events

        not self.debug or self.log.debug(f"Setting result state to : {self.state}")

        kwargs["result"][self.handler.get_index(self)] = self.state
        return super().execute(*args, **kwargs)

    def teardown(self, *args, **kwargs):
        self.event_distributor.remove_callback(self.id, callback=self.new_event)
        super().teardown(*args, **kwargs)
