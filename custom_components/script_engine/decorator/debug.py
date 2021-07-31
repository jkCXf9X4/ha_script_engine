
from custom_components.script_engine.decorator.decorator import Decorator

class Debug(Decorator):
    """
    Sets the debug flag to the decorators after
    """

    def __init__(self, *args, **kwargs):
        super().__init__()  # *args, **kwargs)

        self.decorator_type = "Debug"
        self.name = type(self).__name__

    def get_setup_output(self, *args, **kwargs):
        kwargs["debug"] = True
        return super().get_setup_output(*args, **kwargs)
