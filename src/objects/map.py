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
            raise DuplicateTeamException("teamId " + teamId + "is already in teams.")
        self.teams.append(teamId)

    def addNode(self, node):
        if node.id in self.nodes:
            raise DuplicateNodeException("nodeId " + node.id + "is already in nodes.")
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
        connectedNodes = set()
        getConnectedNodes(startingNode, connectedNodes, startingNode.ownerId)

        totalProcessing = 0
        totalNetworking = 0
        for node in connectedNodes:
            totalProcessing += node.remainingProcessing
            totalNetworking += node.remainingNetworking

        if totalProcessing < processing or totalNetworking < networking:
            raise InsufficientPowerException("networking = %d, processing = %d\nNeeded networking = %d, processing = %d" %
                (totalNetworking, totalProcessing, networking, processing))

        for node in connectedNodes:
            difference = min(processing, remainingProcessing)
            node.remainingProcessing -= difference
            processing -= difference

            difference = min(networking, remainingNetworking)
            node.remainingNetworking -= difference
            networking -= difference

    # recursive function to add all connected nodes to the connectedNodes set
    def getConnectedNodes(self, startingNode, connectedNodes, ownerId):
        if startingNode.ownerId != ownerId or startingNode in connectedNodes:
            return
        connectedNodes.append(startingNode)
        for adjacent in startingNode.adjacentIds:
            getConnectedNodes(self.nodes[adjacent], connectedNodes, ownderId)
