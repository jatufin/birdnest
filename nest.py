import math


class Nest:
    """ A nest object contains the coordinates of the nest and
    the radius of the no fly zone around it.
    """
    def __init__(self,
                 nest_x,
                 nest_y,
                 radius=100):
        """
        Nest class constructor

        Arguments:
        nest_x: float   The x coordinate of the nest (mandatory)
        nest_y: float   The y coordinate of the nest (mandatory)
        radius: Number (default: 100)  Distance from the nest in metres.
                A drone inside the radius is considered a violation
        """
        self.nest_x = nest_x
        self.nest_y = nest_y
        self.radius = radius * 1000  # Convert from metres to millimeters

    def too_close(self, drone_x, drone_y):
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
