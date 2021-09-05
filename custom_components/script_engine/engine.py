
import logging

from homeassistant.core import HomeAssistant

class Engine:
    """
    Handles local variables that can be used in scripts
    """

    def __init__(self, *args, **kwargs) -> None:
        self.hass: HomeAssistant = kwargs.get('hass', None)
        self.log = kwargs.get('logger', logging.getLogger(__name__))
        self.domain = kwargs.get('domain', "unknown_domain")
        self.debug = kwargs.get('debug', False)

    def analyze_events(self, **kwargs):
        e = kwargs.get("events", None)
        if e:
            self.log.info(f"Events: {[str(i) for i in e]}")