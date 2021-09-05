import operator
from typing import Any, Optional, Callable

from custom_components.script_engine.decorator.base_decorator import BaseDecorator

from homeassistant.core import State

class State(BaseDecorator):
    """
    Abstract class that enables a validation of state
    
    Input:
        id: home assistant id

        State, previous_state, bigger_than or smaller_than:
            1.  * - Any, default value
            2.  ** - Any but not None
            3.  text, int, float, custom type, None - try to convert the state to the same type and then compare
            4.  function - will be called without arguments, return value will be evaluated as nr 3.

        custom_eval: function that will be called with custom_eval(self, new_state, old_state) -> True/False
         - self is the script_class self

    """
    def __init__(self, 
            id: str, 
            state: Optional[Any] = "*",
            previous_state: Optional[Any] = "*",
            bigger_than: Optional[Any] = "*",
            smaller_than: Optional[Any] = "*",
            custom_eval: Optional[Callable[[Any, State ,State], bool]] = None,
            custom_eval_condition: Optional[Any] = True,
            stay_valid: Optional[bool] = False,
            *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.decorator_type = "State"
        self.name = type(self).__name__

        self.id = id
        self.required_state = state
        self.required_previous_state = previous_state
        self.required_bigger_than = bigger_than
        self.required_smaller_than = smaller_than
        self.custom_eval = custom_eval
        self.custom_eval_condition = custom_eval_condition
        self.stay_valid = stay_valid

        self.non_value_keys = [None, "*", "**"]

    def __str__(self) -> str:
        return f"{self.name}:{self.id}"

    def setup(self, *args, **kwargs):
        self.valid = False

        self.new_state: State = None
        self.old_state: State = None

        return super().setup(*args, **kwargs)

    def default(self, *args, **kwargs):
        not self.debug or self.log.debug(f"Default state: {self}")

        # Check if new valid check is warranted
        if self.stay_valid == False or (self.stay_valid and self.valid == False):
            self.valid = self.is_valid(self.new_state, self.old_state)
            not self.debug or self.log.debug(f"Valid: {self.valid}")

        if self.valid:
            not self.debug or self.log.debug(f"Decorator is valid, proceding")
            return super().default(*args, **kwargs)
        else:
            not self.debug or self.log.debug(f"Decorator is not valid, aborting")
            return False

    def is_valid(self, new_state: State = None, old_state: State = None):
        
        def has_value(obj):
            is_non_value_key = [i == obj for i in self.non_value_keys]
            return not any(is_non_value_key)

        def evaluate_if_function(obj):
            if callable(obj):
                return obj()
            else:
                return obj

        def convert(obj, t):
            if obj != None:
                if t == bool:
                    if obj == "True":
                        return True
                    else:
                        return False
                else:
                    obj = t(obj)
            return obj

        def check(actual, operation, required):

            # not self.debug or self.log.debug(f"Operation, {operation}")
            # not self.debug or self.log.debug(f"Actual, type {type(actual)}, data: {actual}")

            actual = convert(actual, type(required))

            # not self.debug or self.log.debug(f"Actual, type {type(actual)}, data: {actual}")
            # not self.debug or self.log.debug(f"Required, type {type(required)}, data: {required}")

            if str(required) == "*":
                return True
            elif str(required) == "**" and actual != None:
                return True
            elif str(required) == "**" and actual == None:
                return False
            elif actual != None and operation(actual, required):
                return True
            else:
                return False

        new_state_str = new_state.state if new_state != None else None
        old_state_str = old_state.state if old_state != None else None

        not self.debug or self.log.debug(f"Function: {self.get_wrapped_function_name()}")
        not self.debug or self.log.debug(f"New_state: {new_state}, old state {old_state}")

        required_state = evaluate_if_function(self.required_state)
        required_previous_state = evaluate_if_function(self.required_previous_state)
        required_bigger_than = evaluate_if_function(self.required_bigger_than)
        required_smaller_than = evaluate_if_function(self.required_smaller_than)

        conditions = []
        conditions.append(check(new_state_str, operator.eq, required_state))
        conditions.append(check(old_state_str, operator.eq, required_previous_state))

        # To accurately evaluate time between day limits, ex 22:00 - 06:00
        if has_value(required_bigger_than) and has_value(required_smaller_than) and required_bigger_than >= required_smaller_than:
            not self.debug or self.log.debug(f"Evaluated as time over day limit")
            condition_1 = check(new_state_str, operator.ge, required_bigger_than)
            condition_2 = check(new_state_str, operator.le, required_smaller_than)
            not self.debug or self.log.debug(f"Cond1 {condition_1}, Cond2 {condition_2}")
            conditions.append(condition_1 or condition_2)
        else:
            conditions.append(check(new_state_str, operator.ge, required_bigger_than))
            conditions.append(check(new_state_str, operator.le, required_smaller_than))

        if self.custom_eval != None:
            custom_evaluation = self.custom_eval(self.call_class_self, new_state, old_state) == self.custom_eval_condition
            conditions.append(custom_evaluation)

        not self.debug or self.log.debug(f"Conditions {conditions}")

        if all(conditions):
            return True
        else:
            return False
