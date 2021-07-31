import logging

from homeassistant.core import State

class ServiceExt:

    _logger = logging.getLogger(__name__)

    @classmethod
    def call_service_id(cls, hass, service, action, id, data={}, debug=False):
        data["entity_id"] = id
        not debug or cls._logger.debug(f"Call service, {service}, {action}, {data}")
        hass.services.call(service, action, data)

    @classmethod
    def call_service_data(cls, hass, service, action, data={}, debug=False):
        not debug or cls._logger.debug(f"Call service, {service}, {action}, {data}")
        hass.services.call(service, action, data)
