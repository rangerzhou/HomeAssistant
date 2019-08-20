"""
Weixin Push Service by ServerChan
{"title":"Homeassistant","message":"来自HA的测试"}
{"title":"Homeassistant1824","message":"来自HA的测试![图片](http://www.homeassistant.top:8123/local/mix2.jpg)"}
"""

import logging

import datetime
import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_MESSAGE, ATTR_TITLE, ATTR_DATA, ATTR_TARGET, PLATFORM_SCHEMA, BaseNotificationService)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
_RESOURCE = 'https://pushbear.ftqq.com/sub'

CONF_SCKEY = 'sc_key'

def get_service(hass, config, discovery_info=None):
    """Get the ServerChan notification service."""
    #from fake_useragent import UserAgent

    sc_key = config.get(CONF_SCKEY)
    return ServerchanNotificationService(hass, sc_key)


class ServerchanNotificationService(BaseNotificationService):
    """Implementation of the notification service for SimplePush."""

    def __init__(self, hass, sc_key):
        """Initialize the service."""
        _LOGGER.debug("INIT message")
        self._sc_key = sc_key

    def send_message(self, message='', **kwargs):
        """Send a message to a user."""
        url = '{}/'.format(_RESOURCE)
        title = kwargs.get(ATTR_TITLE)
        if title:
           timestp = datetime.datetime.now()
           sendtitle = '{} {}'.format(timestp.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日'), title)
           send_message = '{} {}'.format(timestp.strftime("%Y-%m-%d %H:%M:%S"), message)
           payload = {'sendkey': self._sc_key, 'text': sendtitle, 'desp': send_message}

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
