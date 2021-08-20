"""
Weixin Push Service by WxPusher
{"title":"Homeassistant","msg":"来自HA的测试"}
"""
import logging

import datetime
import json
import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_MESSAGE, ATTR_TITLE, ATTR_DATA, ATTR_TARGET, PLATFORM_SCHEMA, BaseNotificationService)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
_RESOURCE = 'http://wxpusher.zjiecode.com/api/send/message'

CONF_UIDS = 'uids'
CONF_APPTOKEN = 'apptoken'


def get_service(hass, config, discovery_info=None):
    """Get the ServerChan notification service."""
    uids = config.get(CONF_UIDS)
    apptoken = config.get(CONF_APPTOKEN)
    return WxPusherNotificationService(hass, uids, apptoken)


class WxPusherNotificationService(BaseNotificationService):
    """Implementation of the notification service for SimplePush."""

    def __init__(self, hass, uids, apptoken):
        """Initialize the service."""
        _LOGGER.debug("INIT message")
        self._uids = uids
        self._apptoken = apptoken

    def send_message(self, message='', **kwargs):
        """Send a message to a user."""
        url = _RESOURCE
        title = kwargs.get(ATTR_TITLE)
        if title:
           timestp = datetime.datetime.now()
           sendmessage = '{}'.format(message)
           headers = {'content-type': 'application/json'}
           
           payload = {
                        "appToken": self._apptoken,
                        "content": title+'\n'+sendmessage,
                        "contentType":"1",
                        "topicIds":[ 
                        "null"
                        ],
                        "uids":[
                        self._uids
                        ]
                    }
           response = requests.post(url, data=json.dumps(payload), headers=headers)
           _LOGGER.debug("sneding out message")

           if response.status_code == 1000:
              obj = response.json()
              error_message = obj['error']['message']
              error_code = obj['error']['code']
              _LOGGER.error(
                   "Error %s : %s (Code %s)", resp.status_code, error_message,
                   error_code)
        else:
           timestp = datetime.datetime.now()
           sendmessage = '{}'.format(message)
           headers = {'content-type': 'application/json'}
           
           payload = {
                        "appToken": self._apptoken,
                        "content": sendmessage,
                        "contentType":"1",
                        "topicIds":[ 
                        "null"
                        ],
                        "uids":[
                        self._uids
                        ]
                    }
           response = requests.post(url, data=json.dumps(payload), headers=headers)
           _LOGGER.debug("sneding out message")

           if response.status_code == 1000:
              obj = response.json()
              error_message = obj['error']['message']
              error_code = obj['error']['code']
              _LOGGER.error(
                   "Error %s : %s (Code %s)", resp.status_code, error_message,
                   error_code)
