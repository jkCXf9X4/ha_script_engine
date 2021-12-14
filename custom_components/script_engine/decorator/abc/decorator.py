
from custom_components.script_engine.decorator.decorator_type import DecoratorType
from custom_components.script_engine.decorator.function_handler import FunctionHandler
from custom_components.script_engine.decorator.decorator_handler import DecoratorHandler

from homeassistant.core import HomeAssistant
import logging
import uuid
from enum import Enum
from typing import List


class Decorator:
    """
    Abstract base class for decorators
    Register the decorator to a handler during setup

    """

    def __init__(self, *args, **kwargs):

        self.uuid = uuid.uuid4()
        self.name = type(self).__name__
        self.type = DecoratorType.ABC
        self.log = logging.getLogger(__name__)

        self.debug = kwargs.get("debug", False)

        self.hass: HomeAssistant = None
        self.function: FunctionHandler = None

        self.handler = None

    def __str__(self) -> str:
        return f"{self.name}:{self.type}:wrap's {self.function.get_name()}"

    def __repr__(self) -> str:
        return f"{self.name}:{self.uuid}"

    def __eq__(self, other: object):
        if not isinstance(object, Decorator):
            return NotImplemented
        return self.uuid == other.uuid

    def setup_handler(self, *args, **kwargs):
        if "handler" not in kwargs.keys():
            kwargs["handler"] = DecoratorHandler(debug=self.debug)
        self.handler = kwargs["handler"]
        self.handler.add(self)

        if self.function.is_decorator():
            self.function.call(*args, **kwargs) # Go down chain and register all decorators 

    # Wrapper
    def __call__(self, func):
        self.function = FunctionHandler(func, debug=self.debug)

        def wrapper(*args, **kwargs):
            self.debug = kwargs.get("debug", self.debug)
            self.hass = kwargs.get("hass", self.hass)

            if kwargs.get("setup_handler", False):
                self.function.set_caller(args[0]) 
                self.setup_handler(*args, **kwargs) 
            else:
                self.handler.run(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    def setup(self, *args, **kwargs):
        """Returns new args and kwargs, raise exception if failure to execute"""
        return args, kwargs

    def execute(self, *args, **kwargs):
        """Returns new args and kwargs, raise exception if failure to execute"""
        return args, kwargs

    def teardown(self, *args, **kwargs):
        """Returns new args and kwargs, raise exception if failure to execute"""
        return args, kwargs
