"""
This class binds on to the MM20 server.py file
"""
from gamemap import *
from node import *

# Useful for debugging
import sys
import traceback


class InvalidPlayerException(Exception):
    pass


class AttemptToMultipleDDoSException(Exception):
    pass


class AttemptToMultipleRootkitException(Exception):
    pass


class Game(object):

    def __init__(self, mapPath, totalTurns):
        # Initial values
        #  int
        self.totalTurns = totalTurns
        self.turnsExecuted = 0
        #  dict
        self.queuedTurns = {}
        self.turnResults = {}
        self.playerInfos = {}

        # Load map
        # TODO load map in gamemap() constructor
        self.map = GameMap(mapPath)

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

        # Return response (as a JSON object)
        return (True, {"id": playerId})

    # Add a player's actions to the turn queue
    def queue_turn(self, turnJson, playerId):
        self.queuedTurns[playerId] = turnJson

    # Execute everyone's actions for this turn
    # @returns True if the game is still running, False otherwise
    def execute_turn(self):

        # Execute turns
        self.turnResults = {}
        for playerId in self.queuedTurns:
            turn = self.queuedTurns[playerId]

            # Get actions
            actions = []
            try:
                actions = list(turn.get("actions", []))
            except:
                self.turnResults[playerId] = [{"status": "fail", "messages": "'Actions' parameter must be a list."}]
                continue  # Skip invalid turn

            # Execute actions
            self.turnResults[playerId] = []
            for actionJson in actions:
                action = actionJson.get("action", "").lower()
                targetId = actionJson.get("target", -1)
                multiplier = actionJson.get("multiplier", 1)
                supplierIds = actionJson.get("supplierIds", [])
                actionResult = {"teamId": playerId, "action": action, "targetId": targetId, "multiplier": multiplier}

                try:
                    target = self.map.nodes.get(int(targetId), None)
                    if target:
                        target.targeterId = playerId
                        target.supplierIds = supplierIds

                    powerSources = []
                    if action == "ddos":
                        powerSources = target.doDDoS()
                    elif action == "control":
                        powerSources = target.doControl(multiplier)
                    elif action == "upgrade":
                        powerSources = target.doUpgrade()
                    elif action == "clean":
                        powerSources = target.doClean()
                    elif action == "scan":
                        powerSources = target.doScan()
                    elif action == "rootkit":
                        powerSources = target.doRootkit()
                    elif action == "portScan":
                        powerSources = target.doPortScan()
                    elif action == "ips":
                        target.doIPS()
                    else:
                        actionResult["message"] = "Invalid action type."
                except KeyError:
                    actionResult["message"] = "Invalid node."
                except AttemptToMultipleDDoSException:
                    actionResult["message"] = "Node is already DDoSed."
                except AttemptToMultipleRootkitException:
                    actionResult["message"] = "Node is already rootkitted."
                except InsufficientPowerException:
                    actionResult["message"] = "Insufficient networking and/or processing."
                except IndexError:
                    actionResult["message"] = "Invalid playerID."
                except ValueError:
                    actionResult["message"] = "Type mismatch in parameter(s)."
                except MultiplierMustBePositiveException as e:
                    actionResult["message"] = str(e)
                except Exception as e:
                    raise  # Uncomment me to raise unhandled exceptions
                    actionResult["message"] = "Unknown exception: " + str(e)

                actionResult["status"] = "fail" if "message" in actionResult else "ok"
                if message not in actionResult:
                    actionResult["powerSources"] = powerSourceNodes

                # Record results
                self.turnResults[playerId].append(actionResult)

        # Commit turn results (e.g. DDoSes)
        self.map.resetAfterTurn()

        # Determine winner if appropriate
        done = self.totalTurns > 0 and self.totalTurns <= self.turnsExecuted
        if done:
            for result in self.turnResults.values():
                result.append({"winnerId": 0})  # TODO determine winner + document "turnResults" format

        # Done!
        self.queuedTurns = {}
        self.turnsExecuted += 1
        return not done

    # Return the results of a turn ("server response") for a particular player
    def get_info(self, playerId):
        if playerId not in self.playerInfos:
            raise InvalidPlayerException("Player " + playerId + " doesn't exist.")

        # Get list of nodes visible to player
        isPortScan = playerId in self.map.portScans
        ownedNodes = [x for x in self.map.nodes.values() if isPortScan or x.ownerId == playerId]
        visibleNodes = set(ownedNodes)
        if not isPortScan:
            for n in ownedNodes:
                buff = []
                n.getVisibleNodes(buff)
                visibleNodes.update(buff)

        # TODO document my format!
        return {
            "playerInfo": self.playerInfos[playerId],
            "turnResult": self.turnResults.get(playerId, [{"status": "fail"}, {"message": "No turn executed."}]),
            "map":  [x.toPlayerDict(False) for x in list(visibleNodes)]
        }

    # Return the entire state of the map
    def get_all_info(self):
        return {
            "playerInfos": self.playerInfos,
            "turnResults": [self.turnResults.get(pId, [{"status": "fail"}, {"message": "No turn executed."}]) for pId in self.playerInfos],
            "map":  [x.toPlayerDict(True) for x in self.map.nodes.values()]
        }
