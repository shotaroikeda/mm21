"""
This class binds on to the MM20 server.py file
"""
from gamemap import GameMap as Map
from node import Node as Node


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
        # TODO load map in gamemap() constructor
        self.map = Map(mapPath)

    # Add a player to the game
    def add_new_player(self, jsonObject, playerId):

        # JSON validation
        error = None
        if "teamName" not in jsonObject:
            error = "Missing 'teamName' parameter"
        elif len(jsonObject["teamName"]) == 0:
            error = "'teamName' cannot be an empty string"
        if error:
            return (False, error)

        # Add player to game data
        self.playerInfos[playerId] = jsonObject
        self.playerInfos[playerId]["id"] = playerId
        self.map.addPlayer(playerId)

        # Assign player a random unowned city node
        # TODO make this "fair"
        self.map.getNodesOfType("LargeCity")

        # Return response (as a JSON object)
        return (True, {"id": playerId})

    # Add a player's actions to the turn queue
    def queue_turn(self, turnJson, playerId):
        self.queuedTurns.append(turnJson)

    # Execute everyone's actions for this turn
    # @returns True if the game is still running, False otherwise
    def execute_turn(self):

        # Execute turns
        turnResults = []
        for turn in self.queuedTurns:

            # Values
            move = turn.get("type", "").lower()
            target = self.map.nodes.get(turn.get("target", None), None)
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

    # Return the results of a turn ("server response") for a particular player
    def get_info(self, playerId):
        if playerId not in self.playerInfos:
            raise InvalidPlayerException("Player " + playerId + " doesn't exist.")
        # TODO document my format!
        return {
            "playerInfo": self.playerInfos[playerId],
            "map": [x.toPlayerDict(False) for x in self.map.nodes.values() if x.ownerId == playerId]  # TODO implement port-scanning + rootkit detection
        }

