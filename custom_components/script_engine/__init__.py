"""Home assistant script engine"""

import logging
import sys

from .script_handler import Script_handler
from .misc import FileHandler

from homeassistant.core import (
    HomeAssistant,
)

DOMAIN = "script_engine"

FILE_NAME_PATTERN = 'script_*.py'
FUNCTION_NAME_PATTERN = 'script_*'

SCRIPT_FOLDER = "/config/script_engine/"
CUSTOM_COMPONENTS_FOLDER = FileHandler.get_folder_from__file__(__file__)

async def async_setup(hass: HomeAssistant, config):
    """Set up platform."""

    logger = logging.getLogger(__name__)
    logger.info("Initiating ha script engine module")

    sys.path.append(SCRIPT_FOLDER)
    sys.path.append(CUSTOM_COMPONENTS_FOLDER)

    script_handler = Script_handler(SCRIPT_FOLDER, logger)
    script_handler.find_files(pattern=FILE_NAME_PATTERN)
    script_handler.extract_script_classes()
    script_handler.instantiate_script_classes(hass=hass, logger=logger , domain=DOMAIN)
    script_handler.extract_script_functions(pattern=FUNCTION_NAME_PATTERN)
    script_handler.instantiate_script_functions()

    return True
