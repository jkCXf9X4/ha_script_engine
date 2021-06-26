import logging
from functools import wraps

from .event_distributor import EventDistributor

from .const import FUNCTION_NAME


class AtStateChange:
    def __init__(self, id, to_state, from_state=None):
        self.id = id
        self.to_state = to_state
        self.from_state = from_state

        self.event_evaluation = False

        self.event_distributor = EventDistributor()

        self.setup = True

        self.log = logging.getLogger(__name__)

    def __str__(self):
        return f"{self.id}_{self.to_state}_{self.from_state}"

    def evaluate_state(self, event):
        # id = event.data.get("entity_id")
        new_state = event.data.get("new_state").state
        old_state = event.data.get("old_state")

        if old_state == None:
            return False
        else:
            old_state = old_state.state

        if new_state == self.to_state:
            return True
        else:
            return False

    def __call__(self, func):
        self.wrapped_func = func

        @wraps(self.wrapped_func)
        def callback(*args, **kwargs):
            is_setup = kwargs.get('is_setup', False)

            return_value = False

            if is_setup:

                self.event_distributor.register_callback(self.id, callback=callback)

                return_value = self.wrapped_func(*args, **kwargs)
            else:
                event = kwargs.get("event", None)
                previous_event_evaluation = kwargs.get("previous_event_evaluation", True)

                if previous_event_evaluation:
                    self.event_evaluation = self.evaluate_state(event)

                    if self.event_evaluation:
                        return_value = self.wrapped_func(*args, revious_event_evaluation=self.event_evaluation, **kwargs)

            return return_value

        # callback.__name__ = FUNCTION_NAME + callback.__name__
        return callback
