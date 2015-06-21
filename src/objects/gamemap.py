"""
Holds data about the map
"""

import src.game_constants
import json


class DuplicatePlayerException(Exception):
    pass


class DuplicateNodeException(Exception):
    pass


class InsufficientPowerException(Exception):
    pass


class MapReadException(Exception):
    pass


class GameMap(object):
    def __init__(self, mapPath):

        # Initial values
        self.players = []
        self.nodes = {}  # key = id, value = node

        # Load map file
        #try:
        mapText = None
        with open(mapPath, "r") as f:
            mapText = f.read()
        mapJson = json.loads(mapText)
        #except IOError:
        #    raise MapReadException("Error reading map file {}.".format(mapPath))

        # Store map
        print mapJson
        self.nodes = mapJson["nodes"]

    # Add a player and assign them a starting node
    def addPlayer(self, playerId):
        # Add player
        if playerId in self.players:
            raise DuplicatePlayerException("playerId {} is already in players".format(playerId))
        self.players.append(playerId)
        # Assign node
        startNode = random.choice([x for x in getNodesOfType("Large City") if not x.ownerId])  # TODO make this "fairer"
        startNode.own(playerId)
        # Done!
        return

    # Get all nodes of a given type (e.g. all ISPs)
    def getNodesOfType(self, nodeType):
        return [x for x in nodes if x.nodetype == nodeType]

    # Decrement the power of connected nodes
    # Will raise an exception if the required amount of power is not available
    def decrementPower(self, startingNode, processing, networking):

        # Get connected nodes
        connectedNodes = set()
        getConnectedNodes(startingNode, connectedNodes, startingNode.ownerId)

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
    def getClusteredNodes(self, startNode, clusteredNodes, ownerId):
        if startNode.ownerId != ownerId or startNode in clusteredNodes:
            return
        clusteredNodes.append(startNode)
        for adjacent in startNode.adjacentIds:
            getConnectedNodes(self.nodes[adjacent], clusteredNodes, ownerId)

    # Get all nodes visible to another node
    def getVisibleNodes(self, startNode, visibleNodes, ownerId):
        if startNode in visibleNodes:
            return
        visibleNodes.append(startNode) 
        if startNode.ownerId != ownerId and ownerId not in startNode.rootkits:
            return
        for adjacent in startNode.adjacentIds:
            getVisibleNodes(self.nodes[adjacent], visibleNodes, ownerId)

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
