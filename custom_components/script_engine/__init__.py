"""Home assistant script engine"""

import logging
import sys

async def async_setup(hass, config):
    """
    Extension setup function called by hass during startup
    """
    from custom_components.script_engine.script_handler.script_handler import ScriptHandler
    from custom_components.script_engine.event.event_distributor import EventDistributor

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

    event_distributor = EventDistributor(hass=hass, debug=False)

    script_handler = ScriptHandler(SCRIPT_FOLDER, debug=False)

    def setup():
        script_handler.find_files(pattern=FILE_NAME_PATTERN)
        script_handler.extract_script_classes(pattern=CLASS_NAME_PATTERN)
        script_handler.instantiate_script_classes(hass=hass, domain=DOMAIN)
        script_handler.extract_script_functions(pattern=FUNCTION_NAME_PATTERN)
        script_handler.instantiate_script_functions(setup_handler=True, hass=hass)
        script_handler.instantiate_script_functions(setup=True)

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

