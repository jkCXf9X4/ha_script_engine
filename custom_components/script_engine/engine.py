import importlib
import logging

class Engine:
    """
    Handles local variables that can be used in scripts
    """

    def __init__(self, *args, **kwargs) -> None:
        self.hass = kwargs.get('hass', None)
        self.log = kwargs.get('logger', logging.getLogger(__name__))
        self.domain = kwargs.get('domain', "unknown_domain")
        self.debug = kwargs.get('debug', False)
