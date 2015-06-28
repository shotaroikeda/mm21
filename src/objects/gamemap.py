"""
Holds data about the map
"""

import src.game_constants
import json
import random
from node import *


class DuplicatePlayerException(Exception):
    pass


class DuplicateNodeException(Exception):
    pass


class MapReadException(Exception):
    pass


class MapFormatException(Exception):
    pass


class GameMap(object):
    def __init__(self, mapPath):

        # Initial values
        self.players = []

        # Load map file
        try:
            mapText = None
            with open(mapPath, "r") as f:
                mapText = str(f.read().decode("string-escape").strip('"'))
        except IOError:
            raise MapReadException("Error reading map file {}.".format(mapPath))

        # Store map
        try:
            mapJson = json.loads(mapText)
            self.nodes = {x["id"]: Node(x["id"], x["adjacent-nodes"], x["type"], self) for x in mapJson["nodes"]}
        except:
            raise MapFormatException("Invalid map file format.")

    # Add a player and assign them a starting node
    def addPlayer(self, playerId):

        # Add player
        if playerId in self.players:
            raise DuplicatePlayerException("playerId {} is already in players".format(playerId))
        self.players.append(playerId)

        # Initialize infiltration values
        for n in self.nodes.values():
            n.infiltration[playerId] = 0

        # Assign starting node
        freeNodes = [self.nodes[uid] for uid in self.getNodesOfType("Large City")]  # TODO make this "fairer"
        freeNodes = [x for x in freeNodes if x.ownerId is None]
        startNode = random.choice(freeNodes)
        startNode.own(playerId)
        # startNode.isIPSed = True

        # Done!
        return

    # Get all nodes of a given type (e.g. all ISPs)
    def getNodesOfType(self, nodeType):
        return [uid for uid in self.nodes.iterkeys() if self.nodes[uid].nodetype == nodeType]

    # Reset the map after a turn has finished
    def resetAfterTurn(self):

        # Node updates
        for n in self.nodes.values():

            # Reset remaining resource counts
            n.remainingProcessing = n.processing
            n.remainingNetworking = n.networking

            # Update DDoS status
            n.DDoSed = n.DDoSPending
            n.DDoSPending = False

            # Reset targeter IDs (defensive programming)
            n.targeterId = None

            # Update owned-states
            # We do this here so that people can't conquer a node by being earlier in the turn order
            inf = max(n.infiltration.values())
            if inf > n.totalPower * 2:
                print printColors.GREEN + "Someone conquered something" + printColors.RESET
                maxPlayers = [x for x in n.infiltration if n.infiltration[x] == inf]
                n.own(random.choice(maxPlayers))  # Don't favor lower/higher player IDs - TODO Update the wiki to say "ties will be broken RANDOMLY, not ARBITRARILY"
