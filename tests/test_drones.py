import unittest

from drones import Drones


class TestDrones(unittest.TestCase):
    def setUp(self):
        self.drone = Drones("http://service/drones",
                            "http://service/pilots",
                            250000,
                            250000,
                            radius=100,
                            persist_time=600,
                            time_format="%Y-%m-%dT%H:%M:%S.%fZ")
        
    def test_drone_can_be_created(self):
        self.assertEqual(self.drone.drones_url, "http://service/drones")

    def test_too_close_returns_correct_values(self):
        self.assertEqual(self.drone._too_close(151000, 250000), 99000.0)
        self.assertEqual(self.drone._too_close(150000, 250000), None)
        self.assertEqual(int(self.drone._too_close(225000, 225000)), 35355)        


if __name__ == '__main__':
    unittest.main()
