
from typing import List

from custom_components.script_engine.decorator.base_decorator import BaseDecorator
from custom_components.script_engine.event.event_wrapper import StateChangedEvent

from homeassistant.core import Event, State

class Arguments(BaseDecorator):
    """
    Extracts the event states and wrap's the under the return_name kwarg
    """
    def __init__(self, ids: List[str], key: str, return_name: str = "attributes", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.decorator_type = "Arguments"
        self.name = type(self).__name__

        self.return_name = return_name
        self.ids = ids
        self.key = key

    def get_default_output(self, *args, **kwargs):
        events: List[StateChangedEvent] = kwargs.get("events", [])
        events = [i for i in events if i.entity_id in self.ids]

        attributes_dict = {}
        for i in events:
            attributes_dict[i.entity_id] = i.new_state.attributes[self.key]

        attributes = kwargs.get(self.return_name, [])
        attributes.append(attributes_dict)
        kwargs[self.return_name] = attributes

        return args, kwargs
