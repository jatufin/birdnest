import requests
import xml.etree.ElementTree as ET
import json

from datetime import datetime


class DronesService:
    """ A class to fecth information about the drones and pilots from the server
    """
    def __init__(self,
                 drones_url,
                 pilots_url,
                 time_format="%Y-%m-%dT%H:%M:%S.%fZ"):
        """
        DronesService class constructor

        Arguments:
        drones_url: String. The url for requesting drone XML (mandatory)
        pilots_url: String. The url for requesting pilot XML (mandatory)
        time_format: String  Time formatting used in the drone XML data
        """
        self.drones_url = drones_url
        self.pilots_url = pilots_url
        self.time_format = time_format

        self.pilots_cache = {}

    def get_drones(self):
        """ Get the list of drones from the server

        Returns an dictionary
        """
        root = self._request_xml(self.drones_url)
        result = self._get_drones_from_xml(root)

        return result

    def get_pilot(self, serial_number):
        """ Get information of a pilot from the service

        Arguments:
        serial_number: String  The serial number of the pilot's drone

        Returns:
        A dictionary containing pilot information.
        """
        if serial_number in self.pilots_cache:
            return self.pilots_cache[serial_number]
        
        url = f"{self.pilots_url}{serial_number}"
        result = self._request_json(url)

        if result is not None:
            self.pilots_cache[serial_number] = result

        return result

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
