
from custom_components.script_engine.decorator.abc.decorator import Decorator
from custom_components.script_engine.decorator.decorator_type import DecoratorType

class Duality(Decorator):
    """
    Decorator that enables both true and false to be passed to the function at events under the kwarg["condition"]
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = DecoratorType.POST

        self.condition = None
        self.previous_condition = None

# TODO need rewrite after new handler is introduced
    def execute(self, *args, **kwargs):
        raise NotImplementedError()

        index = self.handler.get_index(self)

        if all(kwargs["result"][:index]):
            kwargs["condition"] = True
            return super().execute(*args, **kwargs)
        else:
            kwargs["result"][:index] = [ True ] * index 
            kwargs["condition"] = False
            return super().execute(*args, **kwargs)

