
from custom_components.script_engine.decorator.abc.decorator import Decorator
from custom_components.script_engine.decorator.decorator_type import DecoratorType

class Debug(Decorator):
    """
    Sets the debug flag to the decorators after in the chain
    """

    def __init__(self, *args, **kwargs):
        super().__init__()  # *args, **kwargs)

        self.type = DecoratorType.OTHER

    def setup(self, *args, **kwargs):
        kwargs["debug"] = True
        return args, kwargs
