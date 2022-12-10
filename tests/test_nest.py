import unittest

from nest import Nest


class TestNest(unittest.TestCase):
    def setUp(self):
        self.nest = Nest(250000, 250000, 100)

    def test_nest_can_be_created(self):
        self.assertEqual(self.nest.radius, 100000)

    def test_too_close_returns_correct_values(self):
        self.assertEqual(self.nest.too_close(151000, 250000),
                         99000.0)
        self.assertEqual(self.nest.too_close(150000, 250000),
                         None)
        self.assertEqual(int(self.nest.too_close(225000, 225000)),
                         35355)


if __name__ == "__main__":
    unittest.main()
