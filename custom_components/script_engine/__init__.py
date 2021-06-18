"""Home assistant script engine"""

"""Home assistant script engine"""

import logging

from .script_handler import Script_handler

from homeassistant.core import (
    HomeAssistant,
)

LOGGER_NAME = __name__

_LOGGER = logging.getLogger(LOGGER_NAME)

DOMAIN = "script_engine"

SCRIPT_NAME_PATTERN = 'hase_*.py'

SCRIPT_FOLDER = "/config/script_engine/"

async def async_setup(hass: HomeAssistant, config):
    """Set up platform."""
    _LOGGER.info("Initiating ha script engine module")

    script_handler = Script_handler(SCRIPT_FOLDER)
    script_handler.find_files(SCRIPT_NAME_PATTERN)
    script_handler.extract_script_classes()
    script_handler.instantiate_script_classes(hass=hass, log_name=LOGGER_NAME )
    script_handler.extract_script_functions()
    script_handler.instantiate_script_functions()
    # hass.states.async_set("script_engine.test1", "its a state")

    # Return boolean to indicate that initialization was successful.
    return True
