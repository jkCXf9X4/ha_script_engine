import operator
from typing import Any, Optional
from collections.abc import Callable

from custom_components.script_engine.decorator.decorator import Decorator

class State(Decorator):
    """
    Abstract class that enables a validation of state
    
    Input:
        id: home assistant id

        State, previous_state, bigger_than or smaller_than:
            1.  text, int, float, custom type, None - try to convert the state to the same type and then compare
            2.  * - Any
            3.  ** - Any but not None
            4.  function - will be called without arguments, return value will be evaluated as 1.

        custom_eval: function that will be called with cusom_eval(new_state, old_state) -> True/False

    """
    def __init__(self, 
            id: str, 
            state: Optional[Any] = "*",
            previous_state: Optional[Any] = "*",
            bigger_than: Optional[Any] = "*",
            smaller_than: Optional[Any] = "*",
            custom_eval: Optional[Callable[[Any ,Any], bool]] = None,
            *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.decorator_type = "State"
        self.name = type(self).__name__

        self.id = id
        self.required_state = state
        self.required_previous_state = previous_state
        self.required_bigger_than = bigger_than
        self.required_smaller_than = smaller_than
        self.cusom_eval = custom_eval

        self.non_value_keys = [None, "*", "**"]

    def __str__(self) -> str:
        return f"{self.name}:{self.id}"

    def has_value(self, required):
        return not any([i == required for i in self.non_value_keys])

    def setup(self, *args, **kwargs):
        self.valid = False

        return super().setup(*args, **kwargs)

    def default(self, *args, **kwargs):
        if self.valid:
            return super().default(*args, **kwargs)
        return False

    def is_valid(self, new_state=None, old_state=None):

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

        # TODO: Looks sloppy, should be fixed
        return_value = True
        return_value = return_value and check_conditions(new_state, operator.eq, self.required_state)
        return_value = return_value and check_conditions(old_state, operator.eq, self.required_previous_state)

        if self.has_value(self.required_bigger_than) and self.has_value(self.required_smaller_than) and self.required_bigger_than >= self.required_smaller_than:
            cond_1 = check_conditions(self.required_bigger_than, operator.ge, new_state)
            cond_2 = check_conditions(self.required_smaller_than, operator.le, new_state)
            return_value = return_value and (cond_1 or cond_2)
        else:
            return_value = return_value and check_conditions(new_state, operator.ge, self.required_bigger_than)
            return_value = return_value and check_conditions(new_state, operator.le, self.required_smaller_than)

        if self.cusom_eval != None:
            return_value = return_value and self.cusom_eval(new_state, old_state)

        return return_value
