import logging

class FunctionHandler:

    def __init__(self, function, debug):
        self.function = function
        self.call_class = None
        self.debug = debug

        self.log = logging.getLogger(__name__)

    # Wrapped function
    def get_name(self):
        return self.function.__name__
    
    def get_module(self):
        return self.function.__module__

    def is_decorator(self):
        return "decorator" in self.get_module()

    def set_caller(self, call_class):
        self.call_class = call_class

    def call(self, *args, **kwargs):
        not self.debug or self.log.debug(f"Call wrapped function {self.get_name()}\n - args: {args}, kwargs: {kwargs}")
        return True if self.function(self.call_class, *args, **kwargs) is not False else False
