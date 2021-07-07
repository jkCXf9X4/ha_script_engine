"""Home assistant script engine"""

import logging
import sys

async def async_setup(hass, config):
    """Set up platform."""
    from custom_components.script_engine.script_handler import ScriptHandler
    from custom_components.script_engine.event_distributor import EventDistributor

    from .const import (
        SCRIPT_FOLDER,
        CLASS_NAME_PATTERN,
        FILE_NAME_PATTERN,
        FUNCTION_NAME_PATTERN,
        DOMAIN,
    )

    logger = logging.getLogger(__name__)
    logger.info("Initiating ha script engine module")

    sys.path.append(SCRIPT_FOLDER)

    event_distributor = EventDistributor(hass=hass)

    script_handler = ScriptHandler(SCRIPT_FOLDER)

    def setup():
        script_handler.find_files(pattern=FILE_NAME_PATTERN)
        script_handler.extract_script_classes(pattern=CLASS_NAME_PATTERN)
        script_handler.instantiate_script_classes(hass=hass, domain=DOMAIN)
        script_handler.extract_script_functions(pattern=FUNCTION_NAME_PATTERN)
        script_handler.instantiate_script_functions(hass=hass, setup=True)

    def teardown():
        script_handler.instantiate_script_functions(teardown=True)
        event_distributor.reset()

    # def reset(call):
    #     """Handle the service call."""
    #     teardown()
    #     setup()

    # hass.services.register(DOMAIN, "Reset", reset)

    setup()

    return True

