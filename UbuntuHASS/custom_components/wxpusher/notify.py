"""
Weixin Push Service by WxPusher
{"title":"Homeassistant","msg":"来自HA的测试"}
"""
import logging

import datetime
import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_MESSAGE, ATTR_TITLE, ATTR_DATA, ATTR_TARGET, PLATFORM_SCHEMA, BaseNotificationService)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
_RESOURCE = 'http://wxmsg.dingliqc.com/send'

CONF_SCKEY = 'userIds'

def get_service(hass, config, discovery_info=None):
    """Get the ServerChan notification service."""
    userIds = config.get(CONF_SCKEY)
    return WxPusherNotificationService(hass, userIds)


class WxPusherNotificationService(BaseNotificationService):
    """Implementation of the notification service for SimplePush."""

    def __init__(self, hass, userIds):
        """Initialize the service."""
        _LOGGER.debug("INIT message")
        self._userIds = userIds

    def send_message(self, message='', **kwargs):
        """Send a message to a user."""
        url = _RESOURCE
        title = kwargs.get(ATTR_TITLE)
        if title:
           timestp = datetime.datetime.now()
           sendmessage = '{}'.format(message)
           payload = {'title': title, 'msg': sendmessage, 'userIds': self._userIds}

           response = requests.get(url,params = payload)
           _LOGGER.debug("sneding out message")
		
           if response.status_code != 200:
              obj = response.json()
              error_message = obj['error']['message']
              error_code = obj['error']['code']
              _LOGGER.error(
                   "Error %s : %s (Code %s)", resp.status_code, error_message,
                   error_code)
        else:
           _LOGGER.error("Title can NOT be null")
