"""
This class translates between JSON and Python stuff
"""

class Game(object)
    def __init__(self):
        self.queuedTurns = []
        return

    # Add a turn (as JSON) to the turn queue
    def queueTurn(turnJson):
        self.queuedTurns.append(turnJson)
        pass
    
    # Execute queued turns and return the resulting JSON
    def executeQueuedTurns():
        results = []
        for turn in self.queuedTurns:
            results.append(executeTurn(turn))
        self.queuedTurns = []
        return

    # Execute a turn and return the resulting JSON
    def executeTurn(turnJson):
        pass

