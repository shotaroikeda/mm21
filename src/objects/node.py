"""
Holds data about a specific node on the map
"""

from game_constants import *
import json as JSON


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

    def canMoveThrough(self, playerId):
        return self.ownerId == playerId or playerId in self.rootkitIds

    def own(self, playerId):
        if playerId == self.ownerId:
            raise Exception("This player owns this node already.")
        self.ownerId = playerId
        self.rootkitIds = []
        for k in self.infiltration:
            self.infiltration[k] = 0
        return
