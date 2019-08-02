# -*- coding: utf-8 -*-
""" Simple Mercedes me API.

"""

import logging
import time
from multiprocessing import RLock
import requests

# from mercedesmejsonpy import Exceptions as mbmeExc

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
logging.basicConfig(filename='logger.log', level=logging.DEBUG)
API_ENDPOINT = "https://api.mercedes-benz.com/experimental/connectedvehicle/v1"
API_VEHICLES = "vehicles"
API_TIRES = "tires"
API_LOCATION = "location"
API_ODOMETER = "odometer"
API_FUEL_STATE = "fuel"
API_CHARGE_STATE = "stateofcharge"
API_DOORS = "doors"
API_TIMEOUT = 10

CONTENT_TYPE_JSON = "application/json;charset=UTF-8"

DOOR_OPTIONS = ["doorstatusfrontleft",
                "doorstatusfrontright",
                "doorstatusrearleft",
                "doorstatusrearright",
                "doorlockstatusfrontleft",
                "doorlockstatusfrontright",
                "doorlockstatusrearleft",
                "doorlockstatusrearright",
                "doorlockstatusdecklid",
                "doorlockstatusgas",
                "doorlockstatusvehicle"]


TIRE_OPTIONS = ["tirepressurefrontleft",
                "tirepressurefrontright",
                "tirepressurerearleft",
                "tirepressurerearright"]

LOCATION_OPTIONS = ["latitude",
                    "longitude",
                    "heading"]

ODOMETER_OPTIONS = ["odometer",
                    "distancesincereset",
                    "distancesincestart",]

# Set to False for testing with tools like fiddler
# Change to True for production
LOGIN_VERIFY_SSL_CERT = True


class Car(object):

    def __init__(self):

        self.id = None
        self.licenseplate = None
        self.finorvin = None
        self.salesdesignation = None
        self.nickname = None
        self.modelyear = None
        self.colorname = None
        self.fueltype = None
        self.powerhp = None
        self.powerkw = None
        self.numberofdoors = None
        self.numberofseats = None
        self.tires = None
        self.odometer = None
        self.fuellevelpercent = None
        self.doors = None
        self.stateofcharge = None
        self.location = None

class StateOfObject(object):
    def __init__(self, unit=None, value=None, retrievalstatus=None, timestamp=None):
        self.unit = None
        self.value = None
        self.retrievalstatus = None
        self.timestamp = None
        if unit is not None:
            self.unit = unit
        if value is not None:
            self.value = value
        if retrievalstatus is not None:
            self.retrievalstatus = retrievalstatus
        if timestamp is not None:
            self.timestamp = timestamp

class Odometer(object):
    def __init__(self):
        self.odometer = None
        self.distancesincereset = None
        self.distancesincestart = None

class Tires(object):
    def __init__(self):
        self.tirepressurefrontleft = None
        self.tirepressurefrontright = None
        self.tirepressurerearleft = None
        self.tirepressurerearright = None

class Doors(object):
    def __init__(self):
        self.doorstatusfrontleft = None
        self.doorstatusfrontright = None
        self.doorstatusrearleft = None
        self.doorstatusrearright = None
        self.doorlockstatusfrontleft = None
        self.doorlockstatusfrontright = None
        self.doorlockstatusrearleft = None
        self.doorlockstatusrearright = None
        self.doorlockstatusdecklid = None
        self.doorlockstatusgas = None
        self.doorlockstatusvehicle = None

class Location(object):
    def __init__(self, latitude=None, longitude=None, heading=None):
        self.latitude = None
        self.longitude = None
        self.heading = None
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if heading is not None:
            self.heading = heading

class CarAttribute(object):
    def __init__(self, value, retrievalstatus, timestamp):
        self.value = value
        self.retrievalstatus = retrievalstatus
        self.timestamp = timestamp

class Controller(object):
    """ Simple Mercedes me API.
    """
    def __init__(self, auth_handler, update_interval, proxies=None):
        _LOGGER.info("Init started")
        self.__lock = RLock()
        self.auth_handler = auth_handler
        self.cars = []
        self.update_interval = update_interval
        self.last_update_time = 0
        self._proxies = proxies
        self._token_info = self.auth_handler.get_cached_token()
        self._auth_header = {"content-type": "application/json",
                             "Authorization": "Bearer {}".format(
                                 self._token_info.get('access_token'))}
        _LOGGER.info("Authorization: %s", self._auth_header)
        self.load_cars()
        _LOGGER.info("Init end")

    def _check_token(self):
        """ Simple Mercedes me API.

        """
        need_token = (self._token_info is None or
                      self.auth_handler.is_token_expired(self._token_info))
        if need_token:
            new_token = \
                self.auth_handler.refresh_access_token(
                    self._token_info['refresh_token'])
            # skip when refresh failed
            if new_token is None:
                return

            self._token_info = new_token
            self._auth_header = {"content-type": "application/json",
                                 "Authorization": "Bearer {}".format(
                                     self._token_info.get('access_token'))}

    def load_cars(self):

        cars = self._retrieve_json_at_url(
            "{}/{}".format(API_ENDPOINT, API_VEHICLES))

        for current_car in cars:
            car = Car()
            car.id = current_car.get('id')
            car.finorvin = current_car.get('finorvin')
            car.licenseplate = current_car.get('licenseplate')

            car_details = self._retrieve_json_at_url(
                "{}/{}/{}".format(API_ENDPOINT,
                                  API_VEHICLES,
                                  current_car.get("id"))
            )

            car.colorname = car_details.get('colorname')
            car.fueltype = car_details.get('fueltype')
            car.nickname = car_details.get('nickname')
            car.modelyear = car_details.get('modelyear')
            car.powerhp = car_details.get('powerhp')
            car.powerkw = car_details.get('powerkw')
            car.salesdesignation = car_details.get('salesdesignation')
            car.numberofdoors = car_details.get('numberofdoors')
            car.numberofseats = car_details.get('numberofseats')

            car.stateofcharge = self.get_state_of_charge(car.id)
            car.doors = self.get_doors(car.id)
            car.tires = self.get_tires(car.id)
            car.location = self.get_location(car.id)
            car.odometer = self.get_odometer(car.id)

            self.cars.append(car)

        self.last_update_time = time.time()

    def update(self):
        """ Simple Mercedes me API. """
        self._check_token()
        self._update_cars()

    def _update_cars(self):
        cur_time = time.time()
        with self.__lock:
            if cur_time - self.last_update_time > self.update_interval:
                for car in self.cars:
                    car.odometer = self.get_odometer(car.id)
                    car.stateofcharge = self.get_state_of_charge(car.id)
                    car.doors = self.get_doors(car.id)
                    car.tires = self.get_tires(car.id)
                    car.location = self.get_location(car.id)

                self.last_update_time = time.time()

    def get_location(self, car_id):
        """ get refreshed location information.

        """
        _LOGGER.debug("get_location for %s called", car_id)

        api_result = self._retrieve_api_result(car_id, API_LOCATION)

        _LOGGER.debug("get_location result: %s", api_result)

        location = Location()

        for loc_option in LOCATION_OPTIONS:
            curr_loc_option = api_result.get(loc_option)
            value = CarAttribute(
                curr_loc_option.get("value"),
                curr_loc_option.get("retrievalstatus"),
                curr_loc_option.get("timestamp"))

            setattr(location, loc_option, value)

        return location

    def get_tires(self, car_id):
        _LOGGER.debug("get_tires for %s called", car_id)

        apiresult = self._retrieve_api_result(car_id, API_TIRES)

        tires = Tires()

        for tire_option in TIRE_OPTIONS:
            curr_tire = apiresult.get(tire_option)
            curr_tire_status = StateOfObject(
                curr_tire.get("unit"),
                curr_tire.get("value"),
                curr_tire.get("retrievalstatus")
            )
            setattr(tires, tire_option, curr_tire_status)

        return tires

    def get_doors(self, car_id):
        _LOGGER.debug("get_doors for %s called", car_id)

        apiresult = self._retrieve_api_result(car_id, API_DOORS)

        doors = Doors()

        for door_option in DOOR_OPTIONS:
            curr_door = apiresult.get(door_option)
            curr_door_status = CarAttribute(
                curr_door.get("value"),
                curr_door.get("retrievalstatus"),
                curr_door.get("timestamp"))
            setattr(doors, door_option, curr_door_status)

        return doors

    def get_odometer(self, car_id):

        _LOGGER.debug("getOdometer for %s called", car_id)
        api_result = self._retrieve_api_result(car_id, API_ODOMETER)

        odometer = Odometer()

        for odometer_option in ODOMETER_OPTIONS:
            option = api_result.get(odometer_option)
            option_status = StateOfObject(option.get("unit"),
                                          option.get("value"),
                                          option.get("retrievalstatus"))
            setattr(odometer, odometer_option, option_status)

        return odometer

    def get_state_of_charge(self, car_id):

        _LOGGER.exception("getStateOfCharge for %s called", car_id)
        stateofcharge = self._retrieve_api_result(car_id, API_CHARGE_STATE)

        result = stateofcharge.get("stateofcharge")
        ret_obj = StateOfObject(result.get("unit"),
                                result.get("value"),
                                result.get("retrievalstatus"))

        _LOGGER.debug("getStateOfCharge for %s finished. Value: %s",
                      car_id,
                      ret_obj.value)

        return ret_obj

    def _retrieve_api_result(self, car_id, api):
        _LOGGER.exception("API_ENDPOINT: %s, APT_VEHICLES: %s, car_id: %s, api: %s", API_ENDPOINT, API_VEHICLES, car_id, api)
        return self._retrieve_json_at_url(
            "{}/{}/{}/{}".format(
                API_ENDPOINT,
                API_VEHICLES,
                car_id,
                api))

    def _retrieve_json_at_url(self, url):
        try:
            _LOGGER.exception("url: %s, headers: %s, proxies: %s", url, self._auth_header, self._proxies)
            logging.debug("Connect to URL %s", str(url))
            res = requests.get(url,
                               headers=self._auth_header,
                               proxies=self._proxies,
                               verify=LOGIN_VERIFY_SSL_CERT)
            _LOGGER.exception("res.json: %s", res.json())
        except requests.exceptions.Timeout:
            _LOGGER.exception(
                "Connection to the api timed out at URL %s", API_VEHICLES)
            return
        if res.status_code != 200:
            _LOGGER.exception(
                "Connection failed with http code %s", res.status_code)
            return
        _LOGGER.debug("Connect to URL %s Status Code: %s", str(url),
                      str(res.status_code))
        return res.json()
