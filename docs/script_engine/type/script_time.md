Module script_engine.type.script_time
=====================================

Classes
-------

`ScriptTime(hours=0, minutes=0, seconds=0)`
:   Time class that can be added and subtracted
    
    All operands return a new SimpleTime
    
    Variable hours can be a timestring with format "12:00" to ensure that the conversion from home assistant is correct

    ### Ancestors (in MRO)

    * custom_components.script_engine.type.simple_time.SimpleTime