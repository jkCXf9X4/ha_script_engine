# Script_Engine

Use as a complete automation engine for home assistant, to replace blueprints and automation schemes in yaml
Create python scripts that use event callbacks from home assistant to trigger scripts

A variant of home assistant "python script" but with a more free for all approach

[Documentation](docs/script_engine/index.md) 

## Simple example use:

A simple example script, 

```
from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState

class _Script_ExampleSimple(Engine):

    @ToState(id="group.family", state="home")
    def _script_is_home(self, *args, **kwargs):
        self.hass.services.call( "light", "turn_on", target = { "entity_id" = "light.living_room" } )

    @ToState(id="group.family", state="not_home")
    def _script_is_away(self, *args, **kwargs):
        self.hass.services.call( "light", "turn_off", target = { "entity_id" = "light.living_room"} )
```
[code](script_engine/examples/script_example_simple.py)

Different decorators can be added for different functions
Decorators can be stacked for an and relationship between the conditions

```
@ToState(id="lock.main", state="unlocked")
@ToState(id="sensor.time", bigger_than=ScriptTime("16:00"))
@ToState(id="group.family", state="home")
def _script_play_1(self, *args, **kwargs):
    StateExt.set_state(self.hass, self.id, "State_1")
    hass.services.call("light", "turn_on", target={"entity_id" = "light.living_room"})
```

A few more advanced uses - [code](script_engine/examples/script_example_advanced.py)


See [docs](docs/script_engine/decorators/index.md) for more info regarding decorators, doc needs more work atm

A few simple wrappers for hass state and service manipulation use are also present for some cleaner use if needed


## Install

Install using hacs, https://hacs.xyz/

Add to configuration.yaml
```
script_engine:
```

Add a folder called "script_engine" to your HA config folder

filename, class name, function names should follow the following patterns
```
FILE_NAME_PATTERN = 'script_*.py'
CLASS_NAME_PATTERN = '_Script_*'
FUNCTION_NAME_PATTERN = '_script_*'
```
