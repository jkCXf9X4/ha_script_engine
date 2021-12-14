
from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState

class _Script_ExampleSimple(Engine):

    @ToState(id="group.family", state="home")
    def _script_is_home(self, *args, **kwargs):
        self.hass.services.call( "light", "turn_on", target = { "entity_id" = "light.living_room" } )

    @ToState(id="group.family", state="not_home")
    def _script_is_away(self, *args, **kwargs):
        self.hass.services.call( "light", "turn_off", target = { "entity_id" = "light.living_room"} )
