
from homeassistant.core import HomeAssistant
import logging
import uuid
from typing import List

class BaseDecorator:
    """
    Abstract base class that handles the decorator chain of execution

    Handles setup, default use and teardown of the decorator

    Info/use case is mainly passed down thru the chain using custom kwargs
    """

    def __init__(self, *args, **kwargs):

        self.uuid = uuid.uuid4()
        self.name = type(self).__name__
        self.decorator_type = "Decorator"

        self.decorators: List[BaseDecorator] = None

        self.debug_from_init = "debug" in kwargs.keys()
        self.debug = kwargs.get("debug", False)

        self.hass: HomeAssistant = None
        self.call_class_self = None

        self.log = logging.getLogger(__name__)

    def __str__(self) -> str:
        return f"{self.name}:{self.decorator_type}:wrap's {self.get_wrapped_function_name}"

    def __repr__(self) -> str:
        return f"{self.name}:{self.uuid}"

    def __call__(self, func):
        """
        
        """
        self.wrapped_func = func

        def wrapper(*args, **kwargs):
            if kwargs.get('setup', False):
                return self.setup(*args, **kwargs)
            elif kwargs.get('teardown', False):
                return self.teardown(*args, **kwargs)
            else:
                return self.default(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    def get_setup_output(self, *args, **kwargs):
        """
        
        """
        kwargs["decorators"] = self.decorators
        return args, kwargs

    def setup(self, *args, **kwargs):
        self.debug = kwargs.get("debug", False) if not self.debug_from_init else self.debug

        self.hass = kwargs.get("hass", None)
        self.call_class_self = args[0]

        self.decorators = kwargs.get("decorators", [])
        self.decorators.append(self)

        if "decorator" in self.wrapped_func.__module__:
            args, kwargs = self.get_setup_output(*args, **kwargs)
            return self.call_wrapped_function(*args, **kwargs)
        else:
            return True

    def get_default_output(self, *args, **kwargs):
        return args, kwargs

    def default(self, *args, **kwargs):
        args, kwargs = self.get_default_output(*args, **kwargs)
        return self.call_wrapped_function(*args, **kwargs)

    def get_teardown_output(self, *args, **kwargs):
        return args, kwargs

    def teardown(self, *args, **kwargs):
        args, kwargs = self.get_teardown_output(*args, **kwargs)
        return self.call_wrapped_function(*args, **kwargs)

    def call_wrapped_function(self, *args, **kwargs):
        not self.debug or self.log.debug(f"Call wrapped function {self.get_wrapped_function_name()}\n - args: {args}, kwargs: {kwargs}")
        return True if self.wrapped_func(self.call_class_self, *args, **kwargs) is not False else False

    def get_wrapped_function_name(self):
        return self.wrapped_func.__name__

    def __eq__(self, other: object):
        if not isinstance(object, BaseDecorator):
            return NotImplemented
        return self.uuid == other.uuid
