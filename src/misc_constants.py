"""
Holds constants used by the server and visualizer
"""

import os


# Helper functions
def path(p):
    return os.path.abspath(os.path.join(os.getcwd(), p))


# Default server port
port = 1337

# Default map
mapFile = path("src/gamerunner/map.json")

# Default logfile path
logFile = path("src/gamerunner/log.json")

# Default client path
defaultClient = path("test-clients/python/")
