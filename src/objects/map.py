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

    # Get all nodes that are clustered with (connected to and of the same team as) another node
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
