import unittest
from unittest.mock import MagicMock
from drones import Drones

from datetime import datetime


class TestDrones(unittest.TestCase):
    def setUp(self):
        self.service = MagicMock()
        self.service.get_drones.return_value = \
            {"serialXXX": {"timestamp": datetime.utcnow(),
                           "positionX": 175000.0,
                           "positionY": 250000.0}}
        self.service.get_pilot.return_value = \
            {"distance": 10000,
             "firstName": "Jean",
             "lastName": "Doe",
             "email": "e@mail"}
        
        self.nest = MagicMock()
        self.nest.too_close.return_value = 50000

        self.drones = Drones(self.service,
                             self.nest,
                             10)
        self.drones.drones = \
            {"serialXXX": {"timestamp": 1,
                           "distance": 10000}}
        
    def test_drone_can_be_created(self):
        self.assertEqual(self.drones.persist_time, 10)

    def test_update_offending_drones_calls_service(self):
        self.drones.update_offending_drones()
        
        self.service.get_drones.assert_called_once()

    def test_get_offending_pilots_calls_service(self):
        self.drones.get_offending_pilots()

        self.service.get_pilot.assert_called_once()



if __name__ == "__main__":
    unittest.main()
