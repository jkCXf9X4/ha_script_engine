import logging

from homeassistant.core import State, HomeAssistant

class ServiceExt:

    _logger = logging.getLogger(__name__)

    @classmethod
    def get_id_dict(cls, id):
        return {["entity_id"]: id}

    @classmethod
    def call_service(cls, hass: HomeAssistant, service, action, service_data=None, target=None, debug=False):
        not debug or cls._logger.debug(f"Call service, {service}, {action}, {service_data}, {target}")
        hass.services.call(service, action, service_data=service_data, target=target)
