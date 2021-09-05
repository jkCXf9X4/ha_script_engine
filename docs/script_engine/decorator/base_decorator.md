Module script_engine.decorator.base_decorator
=============================================

Classes
-------

`BaseDecorator(*args, **kwargs)`
:   Abstract base class that handles the decorator chain of execution
    
    Handles setup, default use and teardown of the decorator
    
    Info/use case is mainly passed down thru the chain using custom kwargs

    ### Methods

    `call_wrapped_function(self, *args, **kwargs)`
    :

    `default(self, *args, **kwargs)`
    :

    `get_default_output(self, *args, **kwargs)`
    :

    `get_setup_output(self, *args, **kwargs)`
    :

    `get_teardown_output(self, *args, **kwargs)`
    :

    `get_wrapped_function_name(self)`
    :

    `setup(self, *args, **kwargs)`
    :

    `teardown(self, *args, **kwargs)`
    :