Module script_engine.type.simple_time
=====================================

Classes
-------

`SimpleTime(hours=0, minutes=0, seconds=0)`
:   Time class that can be added and subtracted
    
    All operands return a new SimpleTime

    ### Class variables

    `hours_per_day`
    :

    `minutes_per_hour`
    :

    `seconds_per_day`
    :

    `seconds_per_hour`
    :

    `seconds_per_minute`
    :

    ### Static methods

    `get_seconds(hours=0, minutes=0, seconds=0)`
    :

    ### Instance variables

    `hour`
    :

    `minute`
    :

    `second`
    :

    `total_seconds`
    :

    ### Methods

    `to_datetime(self) ‑> datetime.datetime`
    :   Get current date with time from simple time

    `to_time(self) ‑> datetime.time`
    :

    `to_timedelta(self) ‑> datetime.timedelta`
    :