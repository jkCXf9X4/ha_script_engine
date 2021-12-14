import operator
from typing import Any, Optional, Callable

from custom_components.script_engine.decorator.abc.valid_decorator import ValidDecorator
from custom_components.script_engine.decorator.decorator_type import DecoratorType
from homeassistant.core import State

class State(ValidDecorator):
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
            persistent: Optional[bool] = False,
            init_valid_state: Optional[bool] = False,
            *args, **kwargs):
        super().__init__(init_valid_state=init_valid_state, persistent=persistent, *args, **kwargs)

        self.id = id
        self.required_event_state = state
        self.required_previous_event_state = previous_state
        self.required_bigger_than = bigger_than
        self.required_smaller_than = smaller_than
        self.custom_eval = custom_eval
        self.custom_eval_condition = custom_eval_condition

        self.non_value_keys = [None, "*", "**"]

        self.new_event_state: State = None
        self.old_event_state: State = None

    def __str__(self) -> str:
        return f"{self.name}:{self.type}:wrap's {self.function.get_name()}, status: {self.state}, new {self.new_event_state}, old {self.old_event_state}"

    def validate(self):
        def has_value(obj):
            is_non_value_key = [i == obj for i in self.non_value_keys]
            return not any(is_non_value_key)

        def evaluate_if_function(obj):
            if callable(obj):
                return obj()
            else:
                return obj

        def convert(obj, t):
            if obj == None:
                return None

            if t == bool: # To ensure str->bool evaluates correctly
                if obj == "True":
                    return True
                else:
                    return False
            else:
                try:
                    return t(obj)
                except:
                    print(f"Cant convert {obj} ({type(obj)}) to {type(t)}")
                    return None


        def check(actual, operation, required):
            actual = convert(actual, type(required))
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

        new_state = self.new_event_state
        old_state = self.old_event_state

        new_state_str = new_state.state if new_state != None else None
        old_state_str = old_state.state if old_state != None else None

        not self.debug or self.log.debug(f"Function: {self.function.get_name()}")
        not self.debug or self.log.debug(f"New_state: {new_state}, old state {old_state}")

        required_state = evaluate_if_function(self.required_event_state)
        required_previous_state = evaluate_if_function(self.required_previous_event_state)
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
