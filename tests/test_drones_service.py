import unittest
from unittest.mock import MagicMock, patch

from src.drones_service import DronesService


class TestDronesService(unittest.TestCase):
    def setUp(self):
        f = open("tests/dronedata.xml")
        self.drones_xml_string = f.read()
        f.close()

        f = open("tests/pilotdata.json")
        self.pilot_json_string = f.read()
        f.close()
       
        self.drone_service = DronesService("http://dronesurl/",
                                           "http://pilotsurl/",
                                           "%Y-%m-%dT%H:%M:%S.%fZ")

    def test_drones_service_is_created_with_correct_state(self):
        self.assertEqual(self.drone_service.drones_url,
                         "http://dronesurl/")
        self.assertEqual(self.drone_service.pilots_url,
                         "http://pilotsurl/")
        self.assertEqual(self.drone_service.time_format,
                         "%Y-%m-%dT%H:%M:%S.%fZ")

    @patch("src.drones_service.requests")
    def test_get_drones_parses_xml_from_server(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = self.drones_xml_string

        mock_requests.get.return_value = mock_response

        result = self.drone_service.get_drones()

        self.assertEqual(result["SN-xHJB8ikDi0"]["model"], "HRP-DRP 1 Pro")
        self.assertEqual(len(result), 3)

    @patch("src.drones_service.requests")
    def test_get_pilot_parses_json_from_server(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = self.pilot_json_string

        mock_requests.get.return_value = mock_response

        result = self.drone_service.get_pilot("P-Ct_UPfW21o")

        self.assertEqual(result["firstName"], "Ludwig")
