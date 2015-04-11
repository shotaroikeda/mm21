"""
This class binds on to the MM20 server.py file
"""


import Map, Node
class InvalidPlayerException(Exception)
    pass

class Game(object):
    def __init__(self):
        self.queuedTurns = []
        self.playerInfos = {}
        return

    # Add a player's actions to the turn queue
    def queue_turn(turnJson):
        self.queuedTurns.append(turnJson)
        return

    # Execute everyone's actions for this turn
    # @returns True if the game is still running, False otherwise
    def execute_turn():
        
        # Execute turns

        # Done!
        self.queuedTurns = []
        return True

    # Return the results of a turn for a particular player
    def get_info(playerId):
        if playerId not in self.playerInfos:
            raise InvalidPlayerException("Player " + playerId + " doesn't exist.")
        return self.playerInfos[playerId]
