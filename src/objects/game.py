"""
This class binds on to the MM20 server.py file
"""
from gamemap import GameMap as Map
from node import Node as Node


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
                actionResult = {}

                try:
                    target = self.map.nodes.get(int(targetId), None)
                    if action == "ddos":
                        target.doDDOS()
                    elif action == "control":
                        target.doControl(player)
                    elif action == "upgrade":
                        target.doUpgrade()
                    elif action == "clean":
                        target.doClean()
                    elif action == "scan":
                        target.doScan()
                    elif action == "rootkit":
                        target.doRootkit(player)
                    elif action == "portScan":
                        map.doPortScan()
                    else:
                        actionResult["message"] = "Invalid action type."
                except KeyError:
                    actionResult["message"] = "Invalid node."
                except AttemptToMultipleDDoSException:
                    actionResult["message"] = "Node is already DDoSed."
                except AttemptToMultipleRootkitException:
                    actionResult["message"] = "Node is already rootkitted."
                except IndexError:
                    actionResult["message"] = "Invalid playerID."
                except ValueError:
                    actionResult["message"] = "Type mismatch in parameter(s)."
                except Exception as e:
                    print e
                    actionResult["message"] = "Unknown exception."

                actionResult["status"] = "fail" if "message" in actionResult else "ok"

                # Record results
                self.turnResults[playerId].append(actionResult)

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
        print self.turnResults.get(playerId, "")
        if playerId not in self.playerInfos:
            raise InvalidPlayerException("Player " + playerId + " doesn't exist.")

        # Get list of nodes visible to player
        ownedNodes = [x for x in self.map.nodes.values() if x.ownerId == playerId]
        visibleNodes = set(ownedNodes)
        for n in ownedNodes:
            buff = []
            self.map.getVisibleNodes(n, buff)
            visibleNodes.update(buff)

        # TODO document my format!
        return {
            "playerInfo": self.playerInfos[playerId],
            "turnResult": self.turnResults[playerId],
            "map": [x.toPlayerDict(False) for x in list(visibleNodes)]  # TODO implement port-scanning + rootkit detection
        }

