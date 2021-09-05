Module script_engine.decorator.to_state
=======================================

Classes
-------

`ToState(id: str, state: Optional[Any] = '*', previous_state: Optional[Any] = '*', bigger_than: Optional[Any] = '*', smaller_than: Optional[Any] = '*', custom_eval: Optional[Callable[[Any, Any], bool]] = None, custom_eval_condition: Optional[Any] = True, stay_valid: Optional[bool] = False, *args, **kwargs)`
:   Decorator that is used to subscribe to and validate event states

    ### Ancestors (in MRO)

    * custom_components.script_engine.decorator.state.State
    * custom_components.script_engine.decorator.base_decorator.BaseDecorator

    ### Methods

    `default(self, *args, **kwargs)`
    :

    `get_default_output(self, *args, **kwargs)`
    :

    `new_event(self, *args, **kwargs)`
    :   Extracts the states from the event, then consuming it to prevent any other decorator from using it
        
        Calls the first decorator and starts the walk down the decorator chain

    `setup(self, *args, **kwargs)`
    :

    `teardown(self, *args, **kwargs)`
    :