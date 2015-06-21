"""
Holds data about a specific node on the map
"""

import game_constants


class Node(object):
    def __init__(self, id, adjacent, nodetype):
        # int
        self.id = id
        self.processing = game_constants.processing[nodeType]
        self.networking = game_constants.networking[nodeType]
        self.totalPower = self.processing + self.networking
        self.remainingProcessing = game_constants.networking[nodeType]
        self.remainingNetworking = game_constants.processing[nodeType]
        self.ownerId = None
        self.softwareLevel = 0
        # int[]
        self.adjacentIds = adjacent
        self.rootkitIds = []
        # bool
        self.DDoSStatus = DDosStatus.NONE
        self.isIPSed = False
        # dict<int, int>
        self.infiltration = dict()
        self.nodetype = nodetype

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
