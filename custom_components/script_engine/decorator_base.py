
import logging

class Decorator:

    def __init__(self, id):
        self.id = id

        self.previous_decorator: Decorator = None
        self.hass = None
        self.base_self = None

        self.log = logging.getLogger(__name__)

        self.valid = False

    def __str__(self):
        return f"{self.id}"

    def are_decorators_valid(self):
        if self.previous_decorator is None:
            return self.valid
        else:
            return self.valid and self.previous_decorator.are_decorators_valid()

    def __call__(self, func):
        self.wrapped_func = func

        def wrapper(*args, **kwargs):  # strange workaround, unable to change name on self.callback
            return self.callback(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    def callback(self, *args, **kwargs):

        if kwargs.get('setup', False):
            self.hass = kwargs.get("hass", None)
            self.previous_decorator = kwargs.get("previous_decorator", None)
            kwargs["previous_decorator"] = self

            self.base_self = args[0]

            return self.setup(*args, **kwargs)

        elif kwargs.get('teardown', False):
            return self.teardown(*args, **kwargs)

        else:  # normal condition
            return self.main(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return self.wrapped_func(*args, **kwargs)

    def main(self, *args, **kwargs):
        return self.wrapped_func(self.base_self, *args, **kwargs)

    def teardown(self, *args, **kwargs):
        return self.wrapped_func(*args, **kwargs)
