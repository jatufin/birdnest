DRONES_URL = "http://assignments.reaktor.com/birdnest/drones"
PILOTS_URL = "http://assignments.reaktor.com/birdnest/pilots/"  # Drone serial number to be concatenated to the end

# Location of the nest (in millimetres)
NEST_X = 250000.0
NEST_Y = 250000.0

# Values given in the assignment: radius=100 and persist_time=600
RADIUS = 100  # No Fly Zone: Radius in metres from the bird's nest
PERSIST_TIME = 600  # Time in seconds. Older detections are filtered out

# Seconds between requesting drone info from the server
# As the server updates the list every two seconds, the polling
# interval must be twice that frequency to catch all drones
POLL_INTERVAL = 1


# Seconds between browser automatic page reload. The page refresh
# does not trigger a drone list request, which is done separately
PAGE_REFRESH = 5

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
