"""
Holds constants used by the core game logic
"""


# NodeType enum (NodeType.Small = 1)
class NodeType:

    processing = {
                   'Map': 0,
                   'Small City': 100,
                   'Medium City': 200,
                   'Large City': 500,
                   'ISP': 2000,
                   'Data Center': 0
                 }

    networking = {
                   'Map': 0,
                   'Small City': 100,
                   'Medium City': 200,
                   'Large City': 500,
                   'ISP': 0,
                   'Data Center': 2000
                 }


# DDoSStatus enum
class DDoSStatus:
    PENDING = 1
    DDOSED = 2
    NONE = 3

# Default number of players
numPlayers = 5
