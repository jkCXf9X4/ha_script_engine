
#!/bin/bash

# Upload changes to home assistant, map config folder as Z:

rm -r Z:\custom_components\script_engine
cp -R $pwd\custom_components\script_engine Z:\custom_components\script_engine 


rm -r Z:\script_engine
cp -R $pwd\script_engine Z:\script_engine

# ssh hassio@192.168.1.113
# ha core restart