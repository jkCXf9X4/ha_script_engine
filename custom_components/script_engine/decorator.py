import functools
import logging
import operator
from enum import Enum
from functools import wraps

from .event_distributor import EventData, EventDistributor
from .decorator_base import Decorator

class IfState(Decorator):
    def __init__(self, id, state="*", previous_state="*", bigger_than="*", smaller_than="*"):
        super().__init__(id)

        self.event_distributor = EventDistributor()

        self.required_state = state
        self.required_previous_state = previous_state
        self.required_bigger_than = bigger_than
        self.required_smaller_than = smaller_than

    def evaluate_state(self, new_state=None, old_state=None):

        def check_conditions(conditions):
            return_value = True

            for (actual, op, required) in conditions:
                if callable(required):
                    required = required()

                if actual != None:
                    # self.log.debug(f"Type actual {type(actual)}, required {type(required)}")
                    t = type(required)
                    actual = t(actual)

                if str(required) == "*":
                    return_value = return_value and True
                elif str(required) == "**" and actual != None:
                    return_value = return_value and True
                elif op(actual, required):
                    return_value = return_value and True
                else:
                    return_value = False

            return return_value

        conditions = []
        conditions.append((new_state, operator.eq, self.required_state))
        conditions.append((old_state, operator.eq, self.required_previous_state))
        conditions.append((new_state, operator.ge, self.required_bigger_than))
        conditions.append((new_state, operator.le, self.required_smaller_than))

        return check_conditions(conditions)

    def setup(self, *args, **kwargs):
        self.event_distributor.register_callback(self.id, callback=self.callback)
        return super().setup(*args, **kwargs)

    def main(self, *args, **kwargs):

        return_value = False

        self.event: EventData = kwargs.get("event", None)

        if self.event != None:
            kwargs.pop("event", None)  # consume event

            old_valid = self.valid
            self.valid = self.evaluate_state(self.event.new_state, self.event.old_state)

            self.log.debug(F"Decorator: {self.id} new event")
            self.log.debug(F"New: {self.event.new_state}, Old: {self.event.old_state}, self.valid: {self.valid}")

            if self.are_decorators_valid() and self.valid != old_valid:
                # self.log.debug(F"Decorator: {self.id} passing to next function")
                return_value = super().main(*args, **kwargs)
        else:
            if self.are_decorators_valid():
                # self.log.debug(F"Decorator: {self.id}, passthru")
                return_value = super().main(*args, **kwargs)

        return return_value
