"""
This class binds on to the MM20 server.py file
"""

import gamemap as Map
import node as Node


class InvalidPlayerException(Exception):
    pass


class Game(object):

    def __init__(self, mapPath, totalTurns):
        # Initial values
        #  int
        self.queuedTurns = []
        self.totalTurns = totalTurns
        self.turnsExecuted = 0
        #  dict
        self.playerInfos = {}

        # Load map
        # TODO @graph-gen team - figure out how we're going to load your map and put that code here

        # Done!
        return

    # Add a player to the game
    def add_new_team(self, jsonObject, player):

        # JSON validation
        error = None
        if "team" not in jsonObject:
            error = "Missing 'team' parameter"
        elif len(jsonObject["team"]) == 0:
            error = "'Team' cannot be an empty string"
        if error:
            return (False, error)

        # Add player to playerInfos
        self.playerInfos[player] = jsonObject

        # Return response (as a JSON object)
        return (True, {"id": player})

    # Add a player's actions to the turn queue
    def queue_turn(self, turnJson, playerId):
        self.queuedTurns.append(turnJson)
        return

    # Execute everyone's actions for this turn
    # @returns True if the game is still running, False otherwise
    def execute_turn(self):

        # Execute turns
        turnResults = []
        for turn in self.queuedTurns:

            # Values
            move = turn.get("type", "").lower()
            target = Map.nodes.get(turn.get("target", None), None)
            result = {}

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
                    result["message"] = "Invalid action type."
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

            # Result status
            result["status"] = "fail" if "message" in result else "ok"
            turnResults.append(result)

        # Done!
        self.queuedTurns = []
        self.turnsExecuted += 1
        return True

    # Return the results of a turn for a particular player
    def get_info(self, playerId):
        if playerId not in self.playerInfos:
            raise InvalidPlayerException("Player " + playerId + " doesn't exist.")
        return self.playerInfos[playerId]
