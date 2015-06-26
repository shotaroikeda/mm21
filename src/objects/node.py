"""
Holds data about a specific node on the map
"""

from game_constants import *
from misc_constants import *
import json as JSON


class AttemptToMultipleDDosException(Exception):
    pass


class AttemptToMultipleRootkitException(Exception):
    pass


class MultiplierMustBePositiveException(Exception):
    pass


class NodeIsDDoSedException(Exception):
    pass


class InsufficientPowerException(Exception):
    pass


class Node(object):
    def __init__(self, id, adjacent, nodetype, gamemap):
        # int
        self.id = id
        self.nodeType = nodetype
        self.processing = NodeType.processing[nodetype]
        self.networking = NodeType.networking[nodetype]
        self.totalPower = self.processing + self.networking
        self.remainingProcessing = self.networking
        self.remainingNetworking = self.processing
        self.ownerId = None
        self.targeterId = None
        self.softwareLevel = 0
        # int[]
        self.adjacentIds = adjacent
        self.rootkitIds = []
        # bool
        self.DDoSed = False
        self.DDoSPending = False
        self.isIPSed = False
        # dict<int, int>
        self.infiltration = dict()
        self.nodetype = nodetype
        # object
        self.map = gamemap

    def getAdjacentNodes(self):
        return [self.map.nodes[nId] for nId in self.adjacentIds]

    def toPlayerDict(self, showRootkits):
        return {
            "id": self.id,
            "processingPower": self.processing,
            "networkingPower": self.networking,
            "owner": self.ownerId,
            "softwareLevel": self.softwareLevel,
            "adjacentIds": self.adjacentIds,
            "isIPSed": self.isIPSed,
            "infiltration": self.infiltration,
            "rootkits": self.rootkits if showRootkits else None
        }

    """
    Map functions
    """
    # Decrement the power of connected nodes
    # @param processing The processing power required
    # @param networking The networking power required
    def decrementPower(self, processing, networking):

        # Get connected nodes
        connectedNodes = []
        for n in self.getAdjacentNodes():
            n.getClusteredNodes(connectedNodes, self.targeterId)

        # Make sure connected nodes have required resource amounts
        totalProcessing = 0
        totalNetworking = 0
        for node in connectedNodes:
            if not node.DDoSed:
                totalProcessing += node.remainingProcessing
                totalNetworking += node.remainingNetworking
        print "Player {}: {} N, {} P".format(self.targeterId, totalProcessing, totalNetworking)
        if totalProcessing < processing or totalNetworking < networking:
            raise InsufficientPowerException("networking = %d, processing = %d\nNeeded networking = %d, processing = %d" % (totalNetworking, totalProcessing, networking, processing))

        # Subtract used resources from connected nodes
        # TODO Let players specify the order in which we go through their nodes for resources
        for node in connectedNodes:
            if node.DDoSed:
                continue
            if processing == 0:
                break
            difference = min(processing, node.remainingProcessing)
            node.remainingProcessing -= difference
            processing -= difference

        for node in connectedNodes:
            if node.DDoSed:
                continue
            if networking == 0:
                break
            difference = min(networking, node.remainingNetworking)
            node.remainingNetworking -= difference
            networking -= difference

    # Get all nodes that are clustered with (connected to and of the same player as) another node
    # @param clusteredNodes (Output) The list of clustered nodes
    # @param ownerId (Optional) Restrict nodes to those owned by this person; if not specified, the owner of the original node will be used
    def getClusteredNodes(self, clusteredNodes, ownerId=None):
        if ownerId is None:
            ownerId = self.ownerId
        if self.ownerId == ownerId and self not in clusteredNodes:
            clusteredNodes.append(self)
            for adjacent in self.getAdjacentNodes():
                adjacent.getClusteredNodes(clusteredNodes, ownerId)

    # Get all nodes visible to (clustered with or adjacent to a cluster containing) another node
    # @param visibleNodes (Output) The list of visible nodes
    def getVisibleNodes(self, visibleNodes, ownerId=None):
        if ownerId is None:
            ownerId = self.ownerId
        if self in visibleNodes:
            return
        visibleNodes.append(self)
        if self.ownerId == ownerId or ownerId in self.rootkitIds:
            for adjacent in self.getAdjacentNodes():
                adjacent.getVisibleNodes(visibleNodes, ownerId)

    # Connect two nodes together
    # @param other The node to connect with
    def connect(self, other):
        # other is a mapNode
        if other.id in self.adjacentIds:
            raise Exception("Nodes are already connected.")
        self.adjacentIds.append(other.id)
        other.adjacentIds.append(self.id)
        return

    # Determine whether a player can move through a node
    # @param playerId The ID of the player
    # @returns True if the player can move through the node, false otherwise
    def canMoveThrough(self, playerId):
        return self.ownerId == playerId or playerId in self.rootkitIds

    # Give control of a node to a player
    # @param playerId The ID of the player
    def own(self, playerId):
        print printColors.GREEN + "Player {} captured Node {} (a {})!".format(playerId, self.id, self.nodeType) + printColors.RESET
        if playerId == self.ownerId:
            raise Exception("This player owns this node already.")
        self.ownerId = playerId
        self.rootkitIds = []
        for k in self.infiltration:
            self.infiltration[k] = 0
        return

    # Consume resources used to perform an action
    # @param processingCost The processing power required
    def requireResources(self, processingCost, networkingCost):
        self.decrementPower(processingCost, networkingCost)

    """
    Player actions
    """
    # Player action to infiltrate (AKA control) a node
    # @param playerId The ID of the infiltrating player
    # @param multiplier The amount of infiltration to performi
    def doControl(self, playerId, multiplier):
        if multiplier <= 0:
            raise MultiplierMustBePositiveException("Multiplier must be greater than 0.")
        if self.DDoSed:
            raise NodeIsDDoSedException("This node is DDoSed and can't be infiltrated.")
        self.requireResources(multiplier, multiplier)
        if playerId == self.ownerId:
            for k in self.infiltration.iterkeys():
                self.infiltration[k] = max(self.infiltration[k] - multiplier, 0)
        else:
            self.infiltration[playerId] = self.infiltration.get(playerId, 0) + multiplier
            if self.infiltration[playerId] > self.totalPower * 2 and self.infiltration[playerId] == max(self.infiltration.values()):
                self.own(playerId)

    # Player action to DDOS a node
    def doDDOS(self):
        self.requireResources(self.totalPower / 5, self.totalPower / 5)
        self.DDoSPending = True

    # Player action to upgrade a node's Software Level
    def doUpgrade(self):
        if self.DDoSed:
            raise NodeIsDDoSedException("This node is DDoSed and can't be upgraded.")
        self.requireResources(self.processing, self.networking)
        self.softwareLevel += 1

    # Player action to clean a node of rootkits
    def doClean(self):
        if self.DDoSed:
            raise NodeIsDDoSedException("This node is DDoSed and can't be cleaned.")
        self.requireResources(100, 0)
        self.rootkitIds = []

    # Player action to scan a node for rootkits
    def doScan(self):
        if self.DDoSed:
            raise NodeIsDDoSedException("This node is DDoSed and can't be scanned.")
        self.requireResources(25, 0)
        return self.rootkitIds

    # Player action to add a rootkit to a node
    # @param playerId The ID of the rootkitting player
    def doRootkit(self, playerId):
        if playerId in self.rootkitIds:
            raise AttemptToMultipleRootkitException("This player has a rootkit here already.")
        if self.DDoSed:
            raise NodeIsDDoSedException("This node is DDoSed and can't be rootkitted.")
        self.requireResources(self.totalPower / 5, self.totalPower / 5)
        self.rootkitIds.append(playerId)

    # Player action to do a port scan
    def doPortScan(self):
        self.requireResources(0, 500)
        return self
