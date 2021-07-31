import functools
import logging
import operator
from enum import Enum
from functools import wraps
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
            *args, **kwargs):
        super().__init__(id, state=state, previous_state=previous_state, bigger_than=bigger_than, smaller_than=smaller_than, custom_eval=custom_eval, *args, **kwargs)

        self.decorator_type = "IfState"
        self.name = type(self).__name__

        self.event_distributor = EventDistributor()

    def setup(self, *args, **kwargs):
        self.event: StateChangedEvent = None
        self.previous_valid = None

        self.event_distributor.register_callback(self.id, callback=self.new_event)
        return super().setup(*args, **kwargs)

    def new_event(self, *args, **kwargs):
        self.event = kwargs.get("event", None)
        kwargs.pop("event", None)  # consume event

        new_state = self.event.new_state.state
        old_state = self.event.old_state.state if self.event.old_state != None else None

        self.valid = self.is_valid(new_state, old_state)
        if self.valid != self.previous_valid:
            self.previous_valid = self.valid

            not self.debug or self.log.debug(F"Decorator: {self.id} new event")
            not self.debug or self.log.debug(F"New: {self.event.new_state}, Old: {self.event.old_state}, Valid: {self.valid}")

            self.decorators[0].default(*args, **kwargs)

    def get_default_output(self, *args, **kwargs):  # overwrite base method
        events = kwargs.get("events", [])
        events.append(self.event)
        kwargs["events"] = events
        return args, kwargs

    def teardown(self, *args, **kwargs):
        self.event_distributor.remove_callback(self.id, callback=self.new_event)
        return super().teardown(*args, **kwargs)
