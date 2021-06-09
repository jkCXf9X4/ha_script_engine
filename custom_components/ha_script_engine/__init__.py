"""Home assistant script engine"""

import logging
_LOGGER = logging.getLogger(__name__)

from datetime import timedelta

DOMAIN = "ha_script_engine"

SCAN_INTERVAL = timedelta(seconds=5)

async def async_setup(hass, config):
    """Set up platform."""
    _LOGGER.info("Initiating ha script engine module")
    hass.states.async_set("ha_script_engine.test1", "its a state")

    # Return boolean to indicate that initialization was successful.
    return True