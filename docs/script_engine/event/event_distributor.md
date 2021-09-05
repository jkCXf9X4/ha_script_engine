Module script_engine.event.event_distributor
============================================

Classes
-------

`EventDistributor(hass: homeassistant.core.HomeAssistant, debug=False)`
:   Subscribes to home assistant event and distributes them to subscribers

    ### Methods

    `register_callback(self, entity_id, callback)`
    :

    `remove_callback(self, entity_id, callback)`
    :

    `reset(self)`
    :