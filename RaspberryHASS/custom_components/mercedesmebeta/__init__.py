"""
Support for MercedesME System.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/mercedesme/
"""
import logging
from datetime import timedelta
import urllib.parse
import base64
import requests
import time

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback
from homeassistant.components.http import HomeAssistantView
from homeassistant.const import (
    CONF_SCAN_INTERVAL, LENGTH_KILOMETERS,
    CONF_EXCLUDE)
from homeassistant.helpers import discovery
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect, dispatcher_send)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_time_interval

REQUIREMENTS = ['mercedesmejsonpy==0.2.4']

DEPENDENCIES = ['http']

_LOGGER = logging.getLogger(__name__)

BINARY_SENSORS = {
#    'doorsClosed': ['Doors closed'],
#    'windowsClosed': ['Windows closed'],
#    'locked': ['Doors locked'],
#    'tireWarningLight': ['Tire Warning'],
#    'warningWashWater': ['Wash Water Warning'],
#    'warningBrakeFluid': ['Brake Fluid Warning'],
#    'warningEngineLight': ['Engine Light Waring'],
#    'trunkClosed': ['Trunk closed'],
#    'trunkLocked': ['Trunk locked'],
#    'fuelLidClosed': ['Fuel Lid closed'],
#    'warningBrakeLineWear': ['Brake Line Wear Warning'],
#    'warningCoolantLevelLow': ['Coolant Level Low Warning'],
#    'parkingBrakeStatus': ['Parking Brake'],
#    'tankReserveLamp': ['Tank Reserve Lamp']
}

SENSORS = {
    'fuellevelpercent': ['Fuel Level', '%', 'fuel', 'fuellevelpercent', 'value'],
    #'fuelRangeKm': ['Fuel Range', LENGTH_KILOMETERS],
    'licenseplate': ['licenseplate', None, None, None, 'licenseplate'],
    'colorname': ['colorname', None, None, None, 'colorname'],    
    'odometer': ['Odometer', 'Km', 'odometer', 'odometer', 'value'],
    'distancesincereset': ['Distance since reset', 'Km', 'odometer', 'distancesincereset', 'value'],
    'distancesincestart': ['Distance since start', 'Km', 'odometer', 'distancesincestart', 'value'],
    #'serviceIntervalDays': ['Next Service', 'days'],
    #'electricRangeKm': ['Electric Range Km', LENGTH_KILOMETERS],
    'stateofcharge_value': ['Electric Charge', '%', None, 'stateofcharge', 'value'],
    #'electricChargingStatus': ['ElectricChargingStatus', None],
    #'electricConsumptionReset': ['Electric Consumption Reset', None],
    #'electricConsumptionStart': ['Electric Consumption Start', None],
    #'distanceElectricalStart': ['Distance Electrical Start', None],
    #'distanceElectricalReset': ['Distance Electrical Reset', None],
    #'lightSwitchPosition': ['Light Switch Position', None],
    'doorstatusfrontleft': ['Door Front Left', None, 'doors', 'doorstatusfrontleft', 'value'],
    'doorstatusfrontright': ['Door Front Right', None, 'doors', 'doorstatusfrontright', 'value'],
    'doorstatusrearleft': ['Door Rear Left', None, 'doors', 'doorstatusrearleft', 'value'],
    'doorstatusrearright': ['Door Rear Right', None, 'doors', 'doorstatusrearright', 'value'],
    'doorlockstatusfrontleft': ['Door Lock Front Left', None, 'doors', 'doorlockstatusfrontleft', 'value'],
    'doorlockstatusfrontright': ['Door Lock Front Right', None, 'doors', 'doorlockstatusfrontright', 'value'],
    'doorlockstatusrearleft': ['Door Lock Front Left', None, 'doors', 'doorlockstatusrearleft', 'value'],
    'doorlockstatusrearright': ['Door Lock Front Right', None, 'doors', 'doorlockstatusrearright', 'value'],
    'doorlockstatusdecklid': ['Door Lock Decklid', None, 'doors', 'doorlockstatusdecklid', 'value'],
    'doorlockstatusgas': ['Door Lock Gas', None, 'doors', 'doorlockstatusgas', 'value'],
    'doorlockstatusvehicle': ['Door Lock Vehicle', None, 'doors', 'doorlockstatusvehicle', 'value'],
    'tirepressurefrontleft': ['Tire Pressure Front Left', None, 'tires', 'tirepressurefrontleft', 'value'],
    'tirepressurefrontright': ['Tire Pressure Front Right', None, 'tires', 'tirepressurefrontright', 'value'],
    'tirepressurerearleft': ['Tire Pressure Rear Left', None, 'tires', 'tirepressurerearleft', 'value'],
    'tirepressurerearright': ['Tire Pressure Rear Right', None, 'tires', 'tirepressurerearright', 'value']
    }


AUTH_CALLBACK_PATH = '/api/mercedesmebeta'
AUTH_CALLBACK_NAME = 'api:mercedesmebeta'
AUTH_SCOPE = 'mb:vehicle:status:general mb:user:pool:reader'

DEFAULT_CACHE_PATH = '.mercedesme-token-cache'

CONF_CACHE_PATH = 'cache_path'
CONF_CLIENT_ID = 'client_id'
CONF_CLIENT_SECRET = 'client_secret'

CONFIGURATOR_LINK_NAME = 'Link MercedesMe account'
CONFIGURATOR_SUBMIT_CAPTION = 'I authorized successfully'
CONFIGURATOR_DESCRIPTION = 'To link your MercedesMe account, ' \
                           'click the link, login, and authorize:'

DATA_MME = 'mercedesmebeta'
DEFAULT_NAME = 'Mercedes ME'
DOMAIN = 'mercedesmebeta'

FEATURE_NOT_AVAILABLE = "The feature %s is not available for your car %s"

NOTIFICATION_ID = 'mercedesme_integration_notification'
NOTIFICATION_TITLE = 'Mercedes me integration setup'

SIGNAL_UPDATE_MERCEDESME = "mercedesme_update"


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_CLIENT_ID): cv.string,
        vol.Required(CONF_CLIENT_SECRET): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=10):
            vol.All(cv.positive_int, vol.Clamp(min=30)),
        vol.Optional(CONF_CACHE_PATH): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def request_configuration(hass, config, oauth):
    """Request Mercedes API authorization."""
    configurator = hass.components.configurator
    hass.data[DOMAIN] = configurator.request_config(
        DEFAULT_NAME, lambda _: None,
        link_name=CONFIGURATOR_LINK_NAME,
        link_url=oauth.get_authorize_url(),
        description=CONFIGURATOR_DESCRIPTION,
        submit_caption=CONFIGURATOR_SUBMIT_CAPTION)

def setup(hass, config):
    """Set up MercedesMe System."""

    from mercedesmejsonpy import oauth
    from mercedesmejsonpy.controller import Controller

    conf = config[DOMAIN]

    scan_interval = conf.get(CONF_SCAN_INTERVAL)

    callback_url = '{}{}'.format(hass.config.api.base_url, AUTH_CALLBACK_PATH)

    cache = config.get(CONF_CACHE_PATH, hass.config.path(DEFAULT_CACHE_PATH))

    auth_handler = oauth.MercedesMeOAuth(conf.get(CONF_CLIENT_ID), 
                            conf.get(CONF_CLIENT_SECRET), 
                            callback_url, AUTH_SCOPE, cache)
    
    token_info = auth_handler.get_cached_token()

    if not token_info:
        _LOGGER.info("no token; requesting authorization")
        hass.http.register_view(MercedesMeAuthCallbackView(
            config, auth_handler))
        request_configuration(hass, config, auth_handler)
        return True

    if hass.data.get(DOMAIN):
        configurator = hass.components.configurator
        configurator.request_done(hass.data.get(DOMAIN))
        del hass.data[DOMAIN]

    mercedesme_api = Controller(auth_handler, scan_interval)
    hass.data[DATA_MME] = MercedesMeHub(mercedesme_api)
    

    discovery.load_platform(hass, 'sensor', DOMAIN, {}, config)
    discovery.load_platform(hass, 'device_tracker', DOMAIN, {}, config)
    #discovery.load_platform(hass, 'binary_sensor', DOMAIN, {}, config )

    def hub_refresh(event_time):
        """Call Mercedes me API to refresh information."""
        _LOGGER.info("Updating Mercedes me component.")
        hass.data[DATA_MME].data.update()
        dispatcher_send(hass, SIGNAL_UPDATE_MERCEDESME)

    track_time_interval(
        hass,
        hub_refresh,
        timedelta(seconds=scan_interval))

    return True

class MercedesMeAuthCallbackView(HomeAssistantView):
    """MercedesMe Authorization Callback View."""

    requires_auth = False
    url = AUTH_CALLBACK_PATH
    name = AUTH_CALLBACK_NAME

    def __init__(self, config, oauth):
        """Initialize."""
        self.config = config
        self.oauth = oauth

    @callback
    def get(self, request):
        """Receive authorization token."""
        hass = request.app['hass']
        self.oauth.get_access_token(request.query['code'])
        hass.async_add_job(setup, hass, self.config)

class MercedesMeHub(object):
    """Representation of a base MercedesMe device."""

    def __init__(self, data):
        """Initialize the entity."""
        self.data = data

class MercedesMeEntity(Entity):
    """Entity class for MercedesMe devices."""

    def __init__(self, data, internal_name, sensor_name, vin, 
                 unit, license, feature_name, object_name, attrib_name):
        """Initialize the MercedesMe entity."""
        self._car = None
        self._data = data
        self._state = False
        self._name = license + ' ' + sensor_name
        self._internal_name = internal_name
        self._unit = unit
        self._vin = vin
        self._feature_name = feature_name
        self._object_name = object_name
        self._attrib_name = attrib_name

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit
