
from custom_components.script_engine.local_event_wrapper import LocalEventWrapper
import logging

from typing import List

import uuid

class Decorator:

    def __init__(self, id, **kwargs):
        self.id = id
        self.uuid = uuid.uuid4()
        self.name = type(self).__name__
        self.decorator_chain: List[Decorator] = None

        self.debug = kwargs.get("debug", False)

        self.hass = None
        self.call_class_self = None

        self.valid = False
        self.previous_valid = None

        self.log = logging.getLogger(__name__)

    def __str__(self):
        return f"{self.name}:{self.id}"

    def __repr__(self) -> str:
        return f"{self.name}:{self.id}:{self.uuid}"

    def is_valid():
        raise NotImplementedError

    def is_chain_valid(self):
        for i in self.decorator_chain:
            if not i.is_valid():
                return False
        return True

    def __call__(self, func):
        self.wrapped_func = func

        def wrapper(*args, **kwargs):  # strange workaround, unable to change name on self.callback
            return self.callback(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    def callback(self, *args, **kwargs):
        if kwargs.get('setup', False):
            return self.setup(*args, **kwargs)

        elif kwargs.get('teardown', False):
            return self.teardown(*args, **kwargs)

        else:
            return self.default(*args, **kwargs)

    def setup(self, *args, **kwargs):
        self.hass = kwargs.get("hass", None)

        self.decorator_chain = kwargs.get("decorator_chain", [])
        self.decorator_chain.append(self)
        kwargs["decorator_chain"] = self.decorator_chain

        self.call_class_self = args[0]
        return self.wrapped_func(*args, **kwargs)

    def default(self, *args, **kwargs):
        self.valid = self.is_valid()
        if self.debug:
            self.log.debug(f" args{args}, kwargs {kwargs}")

        if self.valid == self.previous_valid:
            return  # dont trigger on new events that give the same result
        self.previous_valid = self.valid

        if self.is_chain_valid():
            kwargs["decorators"] = self.decorator_chain
            self.decorator_chain[-1].call_wrapped_function(*args, **kwargs)

    def teardown(self, *args, **kwargs):
        return self.wrapped_func(*args, **kwargs)

    def call_wrapped_function(self, *args, **kwargs):
        if self.debug:
            self.log.debug(f"call wrapped function args{args}, kwargs {kwargs}")
        return self.wrapped_func(self.call_class_self, *args, **kwargs)

    def __eq__(self, other: object):
        if not isinstance(object, Decorator):
            return NotImplemented
        return self.uuid == other.uuid
