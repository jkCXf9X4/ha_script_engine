# Script_Engine

Use as a complete automtaion engine for home assistant, to replace blueprints and automation scheemes in yaml
Create python scripts that use event callbacks from home assistant to trigger scripts

A variant of home assistent "python script" but with a tighter integration into HA



## Simple example use:
'''
@ToState(id="group.family", state="home")
def _script_play_1(self, *args, **kwargs):
    self.log.info("Family is home")
'''

Different decorators can be added for different functions
Decorators can be stacked for an and relationship between the conditions

'''
@ToState(id="lock.main", state="unlocked")
@ToState(id="sensor.time", bigger_than=ScriptTime("16:00"))
@IfState(id="group.family", state="home")
def _script_play_1(self, *args, **kwargs):
    StateExt.set_state(self.hass, self.id, "State_1")
'''

See doc for more info regarding decorators


## Install

Install using hacs, https://hacs.xyz/

Add to configuration.yaml
'''
script_engine:
'''

Add a folder called "script_engine" to your HA config folder 
filename, class name, function names should follow the following patterns
'''
FILE_NAME_PATTERN = 'script_*.py'
CLASS_NAME_PATTERN = '_Script_*'
FUNCTION_NAME_PATTERN = '_script_*'
'''

See (/script_engine/script_example.py) for a full example script
