"""Home assistant script engine"""

import logging
import sys

from .script_handler import Script_handler

from homeassistant.core import (
    HomeAssistant,
)

LOGGER_NAME = __name__

_LOGGER = logging.getLogger(LOGGER_NAME)

DOMAIN = "script_engine"

FILE_NAME_PATTERN = 'script_*.py'
FUNCTION_NAME_PATTERN = 'script_*'

SCRIPT_FOLDER = "/config/script_engine/"

async def async_setup(hass: HomeAssistant, config):
    """Set up platform."""
    _LOGGER.info("Initiating ha script engine module")

    sys.path.append(SCRIPT_FOLDER)

    script_handler = Script_handler(SCRIPT_FOLDER)
    script_handler.find_files( pattern=FILE_NAME_PATTERN)
    script_handler.extract_script_classes()
    script_handler.instantiate_script_classes(hass=hass, log_name=LOGGER_NAME , domain=DOMAIN)
    script_handler.extract_script_functions(pattern=FUNCTION_NAME_PATTERN)
    script_handler.instantiate_script_functions()

    return True
