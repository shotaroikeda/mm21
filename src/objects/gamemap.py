"""
Holds data about the map
"""

import src.game_constants
import json
import random
from node import Node as Node


class DuplicatePlayerException(Exception):
    pass


class DuplicateNodeException(Exception):
    pass


class InsufficientPowerException(Exception):
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
            self.nodes = {x["id"]: Node(x["id"], x["adjacent-nodes"], x["type"]) for x in mapJson["nodes"]}
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
        random.choice(freeNodes).own(playerId)

        # Done!
        return

    # Get all nodes of a given type (e.g. all ISPs)
    def getNodesOfType(self, nodeType):
        return [uid for uid in self.nodes.iterkeys() if self.nodes[uid].nodetype == nodeType]

    # Decrement the power of connected nodes
    # Will raise an exception if the required amount of power is not available
    def decrementPower(self, startingNode, processing, networking):

        # Get connected nodes
        connectedNodes = set()
        self.getConnectedNodes(startingNode, connectedNodes, startingNode.ownerId)

        # Make sure connected nodes have required resource amounts
        totalProcessing = 0
        totalNetworking = 0
        for node in connectedNodes:
            totalProcessing += node.remainingProcessing
            totalNetworking += node.remainingNetworking
        if totalProcessing < processing or totalNetworking < networking:
            raise InsufficientPowerException("networking = %d, processing = %d\nNeeded networking = %d, processing = %d" % (totalNetworking, totalProcessing, networking, processing))

        # Subtract used resources from connected nodes
        for node in connectedNodes:
            if processing == 0:
                break
            difference = min(processing, remainingProcessing)
            node.remainingProcessing -= difference
            processing -= difference

        for node in connectedNodes:
            if networking == 0:
                break
            difference = min(networking, remainingNetworking)
            node.remainingNetworking -= difference
            networking -= difference

    # Get all nodes that are clustered with (connected to and of the same player as) another node
    def getClusteredNodes(self, startNode, clusteredNodes, ownerId=None):
        if not ownerId:
            ownerId = startNode.ownerId
        if startNode.ownerId != ownerId or startNode in clusteredNodes:
            return
        clusteredNodes.append(startNode)
        for adjacent in startNode.adjacentIds:
            self.getConnectedNodes(self.nodes[adjacent], clusteredNodes, ownerId)

    # Get all nodes visible to another node
    def getVisibleNodes(self, startNode, visibleNodes, ownerId=None):
        if not ownerId:
            ownerId = startNode.ownerId
        if startNode in visibleNodes:
            return
        visibleNodes.append(startNode) 
        if startNode.ownerId != ownerId and ownerId not in startNode.rootkitIds:
            return
        for adjacent in startNode.adjacentIds:
            self.getVisibleNodes(self.nodes[adjacent], visibleNodes, ownerId)

    # Reset the map after a turn has finished
    def resetAfterTurn(self):

        # Reset remaining resource counts
        for n in self.nodes:
            node.remainingProcessing = node.processing
            node.remainingNetworking = node.networking

        # Update DDoS status
        for n in self.nodes:
            if self.DDoSStatus == DDoSStatus.PENDING:
                self.DDoSStatus = DDosStatus.DDOSED
            elif self.DDoSStatus == DDoSStatus.DDOSED:
                self.DDoSStatus = DDoSStatus.NONE
