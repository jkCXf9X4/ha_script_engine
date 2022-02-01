
import logging
import uuid
from typing import List

from custom_components.script_engine.decorator.decorator_type import DecoratorType
from custom_components.script_engine.decorator.function_handler import FunctionHandler

from homeassistant.core import HomeAssistant

class DecoratorHandler:
    """
    Handles the decorator chain of execution

    Handles setup, default use and teardown of the decorator
    """

    def __init__(self, *args, **kwargs):

        self.uuid = uuid.uuid4()
        self.name = type(self).__name__

        self.decorators = list()

        self.debug = kwargs.get("debug", False)
        self.log = logging.getLogger(__name__)

        self.script_function: FunctionHandler = None

    def __str__(self) -> str:
        return f"Handler, {self.name}:{self.script_function.get_name()}"

    def __repr__(self) -> str:
        return f"Handler, {self.name}:{self.uuid}"

    def __eq__(self, other: object):
        if not isinstance(object, DecoratorHandler):
            return NotImplemented
        return self.uuid == other.uuid

    def add(self, decorator):
        self.decorators.append(decorator)
        self.script_function = decorator.function # overwrite until last one

    def get_index(self, decorator):
        return self.decorators.index(decorator)

    def run(self, *args, **kwargs):
        if kwargs.get("setup", False):
            self.setup_decorators(*args, **kwargs)      
        elif kwargs.get("teardown"):
            self.teardown_decorators(*args, **kwargs)  
        else:
            self.execute_decorators(*args, **kwargs)

    def setup_decorators(self, *args, **kwargs):
        for i in self.decorators:
            i.setup(*args, **kwargs)

    def teardown_decorators(self, *args, **kwargs):
        for i in self.decorators:
            i.teardown(*args, **kwargs)

    def execute_decorators(self, *args, **kwargs):
        not self.debug or self.log.debug(f"Execute decorators")
        order = [DecoratorType.PRE, DecoratorType.BOOLEAN, DecoratorType.OPERAND, DecoratorType.POST]

        kwargs["result"] = [True] * len(self.decorators)

        if [i for i in self.decorators if i.type == DecoratorType.ABC] != []:
            raise Exception("Decorator is ABC")

        for type_ in order:
            for decorator in self.decorators:
                if decorator.type == type_:
                    not self.debug or self.log.debug(f"Execute decorator nr {decorator}")

                    args, kwargs = decorator.execute(*args, **kwargs)
                    
        if all(kwargs["result"]):
            not self.debug or self.log.debug(f"execute_decorators: result is valid -> calling script function")
            self.script_function.call(*args, **kwargs )
    
