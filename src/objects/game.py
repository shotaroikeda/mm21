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
            if turn["type"] == "ddos":
                try:
                    map.nodes[turn["target"]].doDDOS()
                except KeyError:
                    result["status"] = "fail"
                    result["message"] = "Invalid node."
                except AttemptToMultipleDDosException:
                    result["status"] = "fail"
                    result["message"] = "Attempt to do DDos on a DDosed node."
                except:
                    result["status"] = "fail"
                    result["message"] = "Unknown exception"
                else:
                    result["status"] = "ok"
                    break
               
            elif turn["type"] == "control":
                try:
                    map.nodes[turn["target"]].doControl(player)
                except KeyError:
                    result["status"] = "fail"
                    result["message"] = "Invalid node"
                except IndexError:
                    result["status"] = "fail"
                    result["message"] = "Invalid player Id"
                except:
                    result["status"] = "fail"
                    result["message"] = "Unknown exception"
                else:
                    result["status"] = "ok"
                    break
            
            elif turn["type"] == "upgrade":
                try:
                    map.nodes[turn["target"]].doUpgrade()
                except KeyError:
                    result["status"] = "fail"
                    result["message"] = "Invalid node"
                except:
                    result["status"] = "fail"
                    result["message"] = "Unknown exception"
                else:
                    result["status"] = "ok"
                    break
            
            elif turn["type"] == "clean":
                try:
                    map.nodes[turn["target"]].doClean()
                except KeyError:
                    result["status"] = "fail"
                    result["message"] = "Invalid node"
                except:
                    result["status"] = "fail"
                    result["message"] = "Unknown exception"
                else:
                    result["status"] = "ok"
                    break
        
            elif turn["type"] == "scan":
                try:
                    map.nodes[turn["target"]].doScan()
                except KeyError:
                    result["status"] = "fail"
                    result["message"] = "Invalid  node"
                except:
                    result["status"] = "fail"
                    result["message"] = "Unknown exception"
                else:
                    result["status"] = "ok"
                    break
        
            elif turn["type"] == "rootkit":
                try:
                    map.nodes[turn["target"]].doRootkit(player)
                except KeyError:
                    result["status"] = "fail"
                    result["message"] = "Invalid node"
                except IndexError:
                    result["status"] = "fail"
                    result["message"] = "Invalid playerID"
                except:
                    result["status"] = "fail"
                    result["message"] = "Unknown exception"
                else:
                    result["status"] = "ok"
                    break

            elif turn["type"] == "portScan":
                try:
                    map.doPortScan()
                except:
                    result["status"] = "fail"
                    result["message"] = "Unknown exception"
                else:
                    result["status"] = "ok"
                    break
        
        
        # Done!
        self.queuedTurns = []
        return True

    # Return the results of a turn for a particular player
    def get_info(playerId):
        if playerId not in self.playerInfos:
            raise InvalidPlayerException("Player " + playerId + " doesn't exist.")
        return self.playerInfos[playerId]


