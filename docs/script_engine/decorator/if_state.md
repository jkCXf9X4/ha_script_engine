Module script_engine.decorator.if_state
=======================================

Classes
-------

`IfState(id: str, state: Optional[Any] = '*', bigger_than: Optional[Any] = '*', smaller_than: Optional[Any] = '*', custom_eval: Optional[Callable[[Any, Any], bool]] = None, custom_eval_condition: Optional[Any] = True, stay_valid: Optional[bool] = False, *args, **kwargs)`
:   Decorator that checks if a state is valid

    ### Ancestors (in MRO)

    * custom_components.script_engine.decorator.state.State
    * custom_components.script_engine.decorator.base_decorator.BaseDecorator

    ### Methods

    `default(self, *args, **kwargs)`
    :

    `get_default_output(self, *args, **kwargs)`
    :

    `setup(self, *args, **kwargs)`
    :