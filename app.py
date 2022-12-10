from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from drones import Drones
from config import DRONES_URL, PILOTS_URL, NEST_X, NEST_Y, RADIUS, PERSIST_TIME, POLL_INTERVAL, TIME_FORMAT

from drones_service import DronesService

service = DronesService(DRONES_URL,
                        PILOTS_URL,
                        time_format=TIME_FORMAT)

drones = Drones(service,
                NEST_X,
                NEST_Y,
                radius=RADIUS)


# The drones.update_offending_drones() method is run every POLL_INTERVAL seconds.
# The method updates the list of drones which have detected inside the radius
# from the nest
sched = BackgroundScheduler(daemon=True)
sched.add_job(drones.update_offending_drones, "interval", seconds=POLL_INTERVAL)
sched.start()

app = Flask(__name__)
app.drones = drones


import routes
