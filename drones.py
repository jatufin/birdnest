from datetime import datetime
import copy

       
class Drones:
    """ Main class to acquire information about drones in the vicinity
    and list of drones with pilot information which have breached the
    No Fly Zone
    """
    def __init__(self,
                 service,
                 nest,
                 persist_time=600):
        """
        Drone class constructor

        Arguments:
        service: DronesService  Object for getting information from the server
        nest: Nest  The bidnest around which the No Fly Zone exists
        
        persist_time: Integer (default: 600) Time in seconds after a detected
                violation is disgarded, if drone has not been detected again
        """
        self.service = service
        self.nest = nest
        self.persist_time = persist_time

        self.drones = {}  # A ditionary of detected drones inside the radius

    def update_offending_drones(self):
        """ Request drone information from the server and go through the list
        - If a drone already is in the self.drones dictionary, update the
        timestamp for the drone in the list.
        - If a drone is within the forbidden distance from the nest, but is
        not in the list, add the drone in the self.drones dictionary.
        - Go through self.drones dictionary and remove all drones which have
        timestamp older than self.persist_time
        """
        drones = self.service.get_drones()
        
        for serial_number, properties in drones.items():
            timestamp = properties["timestamp"]

            drone_x = float(properties["positionX"])
            drone_y = float(properties["positionY"])
            distance = self.nest.too_close(drone_x, drone_y)

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
        
        # The dictionary update can happen during iteration, so a copy is used        
        drones = copy.copy(self.drones)
        
        for serial_number, drone in drones.items():
            pilot = self.service.get_pilot(serial_number)
            result.append({"distance": drone["distance"],
                           "firstName": pilot["firstName"],
                           "lastName": pilot["lastName"],
                           "email": pilot["email"],
                           "timestamp": drone["timestamp"]})
        return result
