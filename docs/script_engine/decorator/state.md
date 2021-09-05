Module script_engine.decorator.state
====================================

Classes
-------

`State(id: str, state: Optional[Any] = '*', previous_state: Optional[Any] = '*', bigger_than: Optional[Any] = '*', smaller_than: Optional[Any] = '*', custom_eval: Optional[Callable[[Any, homeassistant.core.State, homeassistant.core.State], bool]] = None, custom_eval_condition: Optional[Any] = True, stay_valid: Optional[bool] = False, *args, **kwargs)`
:   Abstract class that enables a validation of state
    
    Input:
        id: home assistant id
    
        State, previous_state, bigger_than or smaller_than:
            1.  * - Any, default value
            2.  ** - Any but not None
            3.  text, int, float, custom type, None - try to convert the state to the same type and then compare
            4.  function - will be called without arguments, return value will be evaluated as nr 3.
    
        custom_eval: function that will be called with custom_eval(self, new_state, old_state) -> True/False
         - self is the script_class self

    ### Ancestors (in MRO)

    * custom_components.script_engine.decorator.base_decorator.BaseDecorator

    ### Methods

    `default(self, *args, **kwargs)`
    :

    `is_valid(self, new_state: homeassistant.core.State = None, old_state: homeassistant.core.State = None)`
    :

    `setup(self, *args, **kwargs)`
    :