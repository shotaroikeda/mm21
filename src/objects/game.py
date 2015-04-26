"""
This class binds on to the MM20 server.py file
"""

import Map
import Node


class InvalidPlayerException(Exception):
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
        turnResults = []
        for turn in self.queuedTurns:

            # Values
            move = turn["type"].toLower()
            target = map.nodes.get(turn.get("target", None), None)
            results = {}

            # Execute actions
            try:
                if move == "ddos":
                    target.doDDOS()
                elif move == "control":
                    target.doControl(player)
                elif move == "upgrade":
                    target.doUpgrade()
                elif move == "clean":
                    target.doClean()
                elif move == "scan":
                    target.doScan()
                elif move == "rootkit":
                    target.doRootkit(player)
                elif move == "portScan":
                    map.doPortScan()
                else:
                    result["message"] = "Unknown action."
            except KeyError:
                result["message"] = "Invalid node."
            except AttemptToMultipleDDosException:
                result["message"] = "Node is already DDoSed."
            except AttemptToMultipleRootkitException:
                result["message"] = "Node is already rootkitted."
            except IndexError:
                result["message"] = "Invalid playerID."
            except:
                result["message"] = "Unknown exception."

        # Done!
        result["status"] = "fail" if "message" in result else "ok"
        self.queuedTurns = []
        return True

    # Return the results of a turn for a particular player
    def get_info(playerId):
        if playerId not in self.playerInfos:
            raise InvalidPlayerException("Player " + playerId + " doesn't exist.")
        return self.playerInfos[playerId]

i
