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
    def execute_turn(self):

        # Execute turns
        for turn in self.queuedTurns:
            try:
                if turn["type"] == "ddos":
                    map.nodes[turn["target"]].doDDOS()
                elif turn["type"] == "control":
                    map.nodes[turn["target"]].doControl(player)
                elif turn["type"] == "upgrade":
                    map.nodes[turn["target"]].doUpgrade()
                elif turn["type"] == "clean":
                    map.nodes[turn["target"]].doClean()
                elif turn["type"] == "scan":
                    map.nodes[turn["target"]].doScan()
                elif turn["type"] == "rootkit":
                    map.nodes[turn["target"]].doRootkit(player)
                elif turn["type"] == "portScan":
                    map.doPortScan()
                result["status"] = "ok"
            except KeyError:
                result["status"] = "fail"
                result["message"] = "Invalid node."
            except AttemptToMultipleDDosException:
                result["status"] = "fail"
                result["message"] = "Attempt to do " + turn["type"]
            except IndexError:
                result["status"] = "fail"
                result["message"] = "Invalid playerID"
            except:
                result["status"] = "fail"
                result["message"] = "Unknown exception"
        # Done!
        self.queuedTurns = []
        return True

    # Return the results of a turn for a particular player
    def get_info(playerId):
        if playerId not in self.playerInfos:
            raise InvalidPlayerException("Player " + playerId + " doesn't exist.")
        return self.playerInfos[playerId]


