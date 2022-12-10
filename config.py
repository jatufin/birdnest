DRONES_URL = "http://assignments.reaktor.com/birdnest/drones"
PILOTS_URL = "http://assignments.reaktor.com/birdnest/pilots/"  # Drone serial number to be concatenated to the end

# Location of the nest
NEST_X = 250000.0
NEST_Y = 250000.0

# TODO: Correct values radius=100 and persist_time=600
RADIUS = 200  # Radius in metres from the bird's nest
PERSIST_TIME = 60  # Time in seconds. Older detections are filtered out

POLL_INTERVAL = 5  # Seconds between requesting drone info from the server
PAGE_REFRESH = 2  # Seconds between browser automatic page reload

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
