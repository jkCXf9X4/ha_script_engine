import functools
import logging
import operator
from enum import Enum
from functools import wraps

from custom_components.script_engine.event_distributor import EventDistributor
from custom_components.script_engine.local_event_wrapper import LocalEventWrapper
from custom_components.script_engine.decorator.decorator import Decorator

class IfState(Decorator):
    def __init__(self, id, state="*", previous_state="*", bigger_than="*", smaller_than="*", custom_eval=None, **kwargs):
        super().__init__(id, **kwargs)

        self.name = type(self).__name__

        self.event_distributor = EventDistributor()

        self.required_state = state
        self.required_previous_state = previous_state
        self.required_bigger_than = bigger_than
        self.required_smaller_than = smaller_than
        self.cusom_eval = custom_eval

        self.non_value_keys = [None, "*", "**"]

    def has_value(self, required):
        for i in self.non_value_keys:
            if required == i:
                return False
        return True

    def setup(self, *args, **kwargs):
        self.event_distributor.register_callback(self.id, callback=self.new_event)
        self.event = None
        return super().setup(*args, **kwargs)

    def new_event(self, *args, **kwargs):
        self.event: LocalEventWrapper = kwargs.get("event", None)
        kwargs.pop("event", None)  # consume event

        if self.debug:
            self.log.debug(F"Decorator: {self.id} new event")
            self.log.debug(F"New: {self.event.new_state}, Old: {self.event.old_state}, Valid: {self.valid}")

        super().default(*args, **kwargs)

    def is_valid(self):

        def evaluate_state(new_state=None, old_state=None):
            return_value = True
            return_value = return_value and check_conditions(new_state, operator.eq, self.required_state)
            return_value = return_value and check_conditions(old_state, operator.eq, self.required_previous_state)

            if self.has_value(self.required_bigger_than) and self.has_value(self.required_smaller_than) and \
               self.required_bigger_than >= self.required_smaller_than:
                cond_1 = check_conditions(self.required_bigger_than, operator.ge, new_state)
                cond_2 = check_conditions(self.required_smaller_than, operator.le, new_state)
                return_value = return_value and (cond_1 or cond_2)
            else:
                return_value = return_value and check_conditions(new_state, operator.ge, self.required_bigger_than)
                return_value = return_value and check_conditions(new_state, operator.le, self.required_smaller_than)

            if self.cusom_eval != None:
                return_value = return_value and self.cusom_eval(new_state, old_state)

            return return_value

        def check_conditions(actual, op, required):
            if callable(required):
                required = required()

            if actual != None:
                t = type(required)
                actual = t(actual)

            if str(required) == "*":
                return True
            elif str(required) == "**":
                if actual != None:
                    return True
                else:
                    return False
            elif op(actual, required):
                return True
            else:
                return False

        if self.event != None:
            return evaluate_state(self.event.new_state, self.event.old_state)
        else:
            return False



