
from typing import List

from custom_components.script_engine.decorator.abc.decorator import Decorator
from custom_components.script_engine.decorator.decorator_type import DecoratorType
from custom_components.script_engine.event.event_wrapper import StateChangedEvent

from homeassistant.core import Event, State

class Arguments(Decorator):
    """
    Extracts the event states and wrap's the under the return_name kwarg
    """
    def __init__(self, ids: List[str], key: str, return_name: str = "attributes", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.decorator_type = DecoratorType.POST

        self.return_name = return_name
        self.ids = ids
        self.key = key

    def execute(self, *args, **kwargs):
        events: List[StateChangedEvent] = kwargs.get("events", [])
        events = [i for i in events if i.entity_id in self.ids]

        attributes_dict = {}
        for i in events:
            attributes_dict[i.entity_id] = i.new_state.attributes[self.key]

        attributes = kwargs.get(self.return_name, [])
        attributes.append(attributes_dict)
        kwargs[self.return_name] = attributes

        return super().execute(*args, **kwargs)
