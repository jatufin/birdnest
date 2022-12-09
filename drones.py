import math
from datetime import datetime
import copy

import requests
import xml.etree.ElementTree as ET
import json


class Drones:
    def __init__(self,
                 drones_url,
                 pilots_url,
                 nest_x,
                 nest_y,
                 radius=100,
                 persist_time=600,
                 time_format="%Y-%m-%dT%H:%M:%S.%fZ"):
        """
        Drone class constructor

        Arguments:
        drones_url: String. The url for requesting drone XML (mandatory)
        pilots_url: String. The url for requesting pilot XML (mandatory)
        nest_x: float   The x coordinate of the nest (mandatory)
        nest_y: float   The y coordinate of the nest (mandatory)
        radius: Number (default: 100)  Distance from the nest in metres.
                A drone inside the radius is considered a violation
        persist_time: Integer (default: 600) Time in seconds after a detected
                violation is disgarded, if drone has not been detected again
        time_format: String  Time formatting used in the drone XML data
        """
        self.drones_url = drones_url
        self.pilots_url = pilots_url
        self.nest_x = nest_x
        self.nest_y = nest_y
        self.radius = radius * 1000  # Convert from metres to millimeters
        self.persist_time = persist_time
        self.time_format = time_format

        self.drones = {}  # A ditionary of detected drones inside the radius

    def _request_xml(self, url):
        """ Fetch and parse XML data from a given url

        Arguments:
        url: String

        Returns the XML root element
        """
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            return None

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError:
            return None

        return root

    def _request_json(self, url):
        """ Fetch and parse JSON data from a given url

        Arguments:
        url: String

        Returns Python dictionary
        """
        try:
            response = requests.get(url)
            result = json.loads(response.content)
        except requests.exceptions.RequestException:
            return None
        except json.JSONDecodeError:
            return None

        return result

    def _get_drones_from_xml(self, root):
        """ Converts the XML data into a dictionary, where keys are drone serial
        numbers and values dictionaries consisting drone data.

        Arguments:
        root: XML Element object

        Returns a dictionary
        """
        result = {}
        timestamp_string = root[1].attrib["snapshotTimestamp"]
        timestamp = datetime.strptime(timestamp_string, self.time_format)

        for child in root[1]:
            drone = {"timestamp": timestamp}
            for property in child:
                drone[property.tag] = property.text
            result[drone["serialNumber"]] = drone

        return result


    def update_offending_drones(self):
        """ Request drone information from the server and go through the list
        - If a drone already is in the self.drones dictionary, update the
        timestamp for the drone in the list.
        - If a drone is within the forbidden distance from the nest, but is
        not in the list, add the drone in the self.drones dictionary.
        - Go through self.drones dictionary and remove all drones which have
        timestamp older than self.persist_time
        """
        root = self._request_xml(self.drones_url)
        drones = self._get_drones_from_xml(root)
        print(f"DRONES: {drones}")
        
        for serial_number, properties in drones.items():
            timestamp = properties["timestamp"]

            drone_x = float(properties["positionX"])
            drone_y = float(properties["positionY"])
            distance = self._too_close(drone_x, drone_y)

            # The drone is already in the list of drones too close
            if serial_number in self.drones:
                self.drones[serial_number]["timestamp"] = timestamp
                if distance is not None and \
                   distance < self.drones[serial_number]["distance"]:
                    self.drones[serial_number]["distance"] = distance
                continue

            # The distance was not too close
            if distance is None:
                continue

            # The drone is added first time to the list of drones too close
            self.drones[serial_number] = {
                "timestamp": timestamp,
                "distance": distance
                }

        self._remove_old_drones()
        print("\nOFFENDING DRONES:\n", self.drones)

    def _remove_old_drones(self):
        """ Go through the drone list and remove ones, which have not been
        detected since self.persist seconds
        """
        now = datetime.utcnow()

        to_be_deleted = []

        for serial_number, drone in self.drones.items():
            age = now - drone["timestamp"]
            if age.total_seconds() > self.persist_time:
                to_be_deleted.append(serial_number)

        for serial_number in to_be_deleted:
            del self.drones[serial_number]

    def get_offending_pilots(self):
        """ Get a list of all pilots whose drones have been too close
        to the nest

        Returns:
        A list of dictionaries containing drone distance and
        pilot information
        """
        result = []
        
        # The dictionary can be updated during iteration, so a copy is used        
        drones = copy.copy(self.drones)
        
        for serial_number, drone in drones.items():
            pilot = self.get_pilot(serial_number)
            result.append({"distance": drone["distance"],
                           "firstName": pilot["firstName"],
                           "lastName": pilot["lastName"],
                           "email": pilot["email"],
                           "timestamp": drone["timestamp"]})
        return result

    def get_pilot(self, serial_number):
        """ Get information of a pilot from the service

        Arguments:
        serial_number: String  The serial number of the pilot's drone

        Returns:
        A dictionary containing pilot information.
        """
        url = f"{self.pilots_url}{serial_number}"

        result = self._request_json(url)

        return result

    def _too_close(self, drone_x, drone_y):
        """ Measures the distance of the drone from the nest
        and returns the distance in metres

        Arguments:
        drone_x: Integer  The x coordinate of the drone position
        drone_y: Integer  The y coordinate of the drone position

        Returns:
        Integer. Distance in metres to the nest if too close, otherwise None
        """
        distance = math.sqrt((drone_x - self.nest_x)**2 +
                             (drone_y - self.nest_y)**2)

        if distance < self.radius:
            return distance

        return None
