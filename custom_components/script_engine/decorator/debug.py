
from custom_components.script_engine.decorator.base_decorator import BaseDecorator

class Debug(BaseDecorator):
    """
    Sets the debug flag to the decorators after in the chain
    """

    def __init__(self, *args, **kwargs):
        super().__init__()  # *args, **kwargs)

        self.decorator_type = "Debug"
        self.name = type(self).__name__

    def get_setup_output(self, *args, **kwargs):
        kwargs["debug"] = True
        return super().get_setup_output(*args, **kwargs)
