#!/bin/bash

# Upload changes to home assistant

rm -r Z:\custom_components\script_engine
cp -R C:\Users\Rosen\Dropbox\Arbete\SOURCE\ha_script_engine\custom_components\script_engine Z:\custom_components\script_engine 


rm -r Z:\script_engine
cp -R C:\Users\Rosen\Dropbox\Arbete\SOURCE\ha_script_engine\script_engine Z:\script_engine


# Restart ha core

# ssh hassio@192.168.1.113
# ha core restart