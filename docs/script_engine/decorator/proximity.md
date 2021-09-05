Module script_engine.decorator.proximity
========================================

Classes
-------

`Proximity(hours=0, minutes=1, *args, **kwargs)`
:   Decorator that ensures that a function can not be called to closely again

    ### Ancestors (in MRO)

    * custom_components.script_engine.decorator.base_decorator.BaseDecorator

    ### Methods

    `default(self, *args, **kwargs)`
    :

    `time_inside_frame_from_timeframe_to_now(dt: datetime.datetime, hours=0, minutes=0)`
    :