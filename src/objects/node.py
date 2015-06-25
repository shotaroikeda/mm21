"""
Holds data about a specific node on the map
"""

from game_constants import *
import json as JSON


class AttemptToMultipleDDosException(Exception):
    pass


class AttemptToMultipleRootkitException(Exception):
    pass


class MultiplierMustBePositiveException(Exception):
    pass


class Node(object):
    def __init__(self, id, adjacent, nodetype):
        # int
        self.id = id
        self.processing = NodeType.processing[nodetype]
        self.networking = NodeType.networking[nodetype]
        self.totalPower = self.processing + self.networking
        self.remainingProcessing = self.networking
        self.remainingNetworking = self.processing
        self.ownerId = None
        self.softwareLevel = 0
        # int[]
        self.adjacentIds = adjacent
        self.rootkitIds = []
        # bool
        self.DDoSStatus = DDoSStatus.NONE
        self.isIPSed = False
        # dict<int, int>
        self.infiltration = dict()
        self.nodetype = nodetype

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
        map.decrementPower(self, self.processingCost, self.networkingCost)

    # Player action to infiltrate (AKA control) a node
    # @param playerId The ID of the infiltrating player
    # @param multiplier The amount of infiltration to performi
    def doControl(self, playerId, multiplier):
        if multiplier <= 0:
            raise MultiplierMustBePositiveException("Multiplier must be greater than 0.")
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
        if self.DDoSStatus == DDoSStatus.PENDING:
            raise AttemptToMultipleDDosException() 
        self.requireResources(self.totalPower / 5, self.totalPower / 5)
        self.DDoSStatus = DDoSStatus.PENDING

    # Player action to upgrade a node's Software level
    def doUpgrade(self):
        self.requireResources(self.processing, self.networking)
        self.softwareLevel += 1

    # Player action to clean a node of rootkits
    def doClean(self):
        self.requireResources(100, 0)
        self.rootkitIds = []

    # Player action to scan a node for rootkits
    def doScan(self):
        return self.rootkitIds

    # Player action to add a rootkit to a node
    # @param playerId The ID of the rootkitting player
    def doRootkit(self, playerId):
        if playerId in self.rootkitIds:
            raise AttemptToMultipleRootkitException("This player has a rootkit here already.")
        self.requireResources(self.totalPower / 5, self.totalPower / 5)
        self.rootkitIds.append(playerId)

    # Player action to do a port scan
    def doPortScan(self):
        self.requireResources(0, 500)
        return self
