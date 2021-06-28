import functools
import logging
from functools import wraps
from enum import Enum

from .event_distributor import EventDistributor

class StateData:
    def __init__(self, id=None, new_state=None, old_state=None, event=None) -> None:
        self.id = id
        self.new_state = new_state
        self.old_state = old_state
        if event is not None:
            self.id, self.new_state, self.old_state = self.extract_event_states(event)

    def extract_event_states(self, event):
        id = event.data.get("entity_id")
        new_state = event.data.get("new_state").state
        old_state = event.data.get("old_state")

        if old_state != None:
            old_state = old_state.state

        return id, new_state, old_state

class EventDecorator:

    def __init__(self, id):
        self.id = id

        self.persistent_state = False
        self._is_valid = False

        self.event_distributor = EventDistributor()
        self.state = None

        self.previous_decorator: EventDecorator = None
        self.hass = None

    def __str__(self):
        return f"{self.id}"

    def set_persitent_state(self, bool):
        self.persistent_state = bool

    def evaluate_state(self, event_data: StateData):
        raise NotImplementedError()

    def is_valid(self):
        if self.previous_decorator is None:
            return self._is_valid
        else:
            return self._is_valid and self.previous_decorator.is_valid()

    def __call__(self, func):
        self.wrapped_func = func

        @wraps(self.wrapped_func)
        def temp(*args, **kwargs):
            self.callback(*args, **kwargs)

        return temp  # functools.update_wrapper(temp, func)

    def callback(self, *args, **kwargs):

        return_value = False

        if kwargs.get('setup', False):
            return_value = self.setup(*args, **kwargs)

        elif kwargs.get('teardown', False):
            return_value = self.teardown(*args, **kwargs)

        else:  # normal condition
            return_value = self.main(*args, **kwargs)

        if not self.persistent_state:
            self._is_valid = False

        return return_value

    def setup(self, *args, **kwargs):
        self.previous_decorator = kwargs.get("previous_decorator", None)
        self.hass = kwargs.get("hass", None)

        self.event_distributor.register_callback(self.id, callback=self.callback)

        value = self.wrapped_func(*args, previous_decorator=self, **kwargs)

        self.state = StateData(id=self.id, new_state=self.hass.states.get(self.id))
        self._is_valid = self.evaluate_state(self.state)

        return value

    def main(self, *args, **kwargs):
        event = kwargs.get("event", None)

        return_value = False
        
        if event is not None:
            self.state = StateData(event)
            self._is_valid = self.evaluate_state(self.state)

            kwargs.pop("event", None)  # consume event

        if self.is_valid():
            return_value = self.wrapped_func(*args, **kwargs)

        return return_value

    def teardown(self, *args, **kwargs):
        return self.wrapped_func(*args, **kwargs)

class ToState(EventDecorator):
    def __init__(self, id, to_state, from_state="*"):
        super().__init__(id)

        self.to_state = to_state
        self.from_state = from_state

    def evaluate_state(self, state_data: StateData):
        if state_data.new_state == self.to_state:
            if self.from_state == "*":
                if state_data.old_state is not None:
                    return True
            elif self.from_state == state_data.old_state:
                return True

        return False

class AtState(EventDecorator):
    def __init__(self, id, valid_state):
        super().__init__(id)

        self.valid_state = valid_state

        self.set_persitent_state(True)

    def evaluate_state(self, state_data: StateData):
        if state_data.new_state == self.valid_state:
            return True
        return False


# class AtStateChange:
#     def __init__(self, id, to_state, from_state=None):
#         self.id = id
#         self.to_state = to_state
#         self.from_state = from_state

#         self.event_evaluation = False

#         self.event_distributor = EventDistributor()

#         self.setup = True

#         self.log = logging.getLogger(__name__)

#     def __str__(self):
#         return f"{self.id}_{self.to_state}_{self.from_state}"

#     def evaluate_state(self, event):
#         # id = event.data.get("entity_id")
#         new_state = event.data.get("new_state").state
#         old_state = event.data.get("old_state")

#         if old_state == None:
#             return False
#         else:
#             old_state = old_state.state

#         if new_state == self.to_state:
#             return True
#         else:
#             return False

#     def __call__(self, func):
#         self.wrapped_func = func

#         @wraps(self.wrapped_func)
#         def callback(*args, **kwargs):
#             is_setup = kwargs.get('is_setup', False)

#             return_value = False

#             if is_setup:

#                 self.event_distributor.register_callback(self.id, callback=callback)

#                 return_value = self.wrapped_func(*args, **kwargs)
#             else:
#                 event = kwargs.get("event", None)
#                 previous_event_evaluation = kwargs.get("previous_event_evaluation", True)

#                 if previous_event_evaluation:
#                     self.event_evaluation = self.evaluate_state(event)

#                     if self.event_evaluation:
#                         return_value = self.wrapped_func(*args, revious_event_evaluation=self.event_evaluation, **kwargs)

#             return return_value

#         # callback.__name__ = FUNCTION_NAME + callback.__name__
#         return callback
