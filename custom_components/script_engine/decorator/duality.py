
from custom_components.script_engine.decorator.base_decorator import BaseDecorator

class Duality(BaseDecorator):
    """
    Decorator that enables both true and false to be passed to the function at events under the kwarg["condition"]
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.decorator_type = "Duality"
        self.name = type(self).__name__

        self.condition = None
        self.previous_condition = None

    def default(self, *args, **kwargs):
        kwargs["condition"] = True
        self.condition = super().default(*args, **kwargs)

        if self.previous_condition != self.condition and self.condition is False:
            kwargs["condition"] = False

            for i in self.decorators:
                args, kwargs = i.get_default_output(*args, **kwargs)

            self.decorators[-1].call_wrapped_function(*args, **kwargs)

        self.previous_condition = self.condition
        return self.condition
