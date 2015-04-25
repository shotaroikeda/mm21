"""
Holds data about the map
"""

import game_constants


class DuplicateTeamException(Exception):
    pass


class DuplicateNodeException(Exception):
    pass


class InsufficientPowerException(Exception):
    pass


class Map(object):
    def __init__(self):
        self.teams = []
        # key = id, value = node
        self.nodes = {}

    # Add a team and assign them a starting node
    def addTeam(self, teamId):
        if teamId in self.teams:
            raise DuplicateTeamException(
                "teamId {} is already in teams".format(teamId))
        self.teams.append(teamId)

    def addNode(self, node):
        if node.id in self.nodes:
            raise DuplicateNodeException(
                "nodeId {} is already in nodes.".format(node.id))
        self.nodes[node.id] = node

    # Get all nodes of a given type (e.g. all ISPs)
    def getNodesOfType(self, nodeType):
        nodesOfType = []
        for node in self.nodes.itervalues():
            if node.nodetype == nodeType:
                nodesOfType.append(node)
        return nodesOfType

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
            raise InsufficientPowerException("networking = %d, processing = %d\nNeeded networking = %d, processing = %d" %
                (totalNetworking, totalProcessing, networking, processing))

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

    # Get all nodes of a particular team that are connected to another node
    def getConnectedNodes(self, startingNode, connectedNodes, ownerId):
        if startingNode.ownerId != ownerId or startingNode in connectedNodes:
            return
        connectedNodes.append(startingNode)
        for adjacent in startingNode.adjacentIds:
            getConnectedNodes(self.nodes[adjacent], connectedNodes, ownderId)

    # Get all nodes visible to another node
    def getVisibleNodes(self, startingNode, visibleNodes, ownerId):
        visibleNodes.append(startingNode) 
        if (startingNode.ownerId != ownerId and ownerId not in startingNode.rootkits) or startingNode in visibleNodes:
            return
        for adjacent in startingNode.adjacentIds:
            getVisibleNodes(self.nodes[adjacent], visibleNodes, ownderId)

    # Reset the map after a turn has finished
    def resetAfterTurn(self):

        # Reset remaining resource counts
        for n in self.nodes:
            node.remainingProcessing = node.processing
            node.remainingNetworking = node.networking


